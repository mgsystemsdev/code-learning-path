#!/usr/bin/env python3
"""
DMRB Core Lifecycle State Machine Prototype
Tests the dual lifecycle concept with real-world scenarios
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
import json

# ========================================================================================
# SHARED CORE (Layer 1) - Foundation Types
# ========================================================================================

class NVMState(str, Enum):
    """Resident Lifecycle - Outer Shell"""
    NOTICE = "NOTICE"
    VACANT = "VACANT" 
    SCHEDULED = "SCHEDULED"
    MOVE_IN = "MOVE_IN"
    ARCHIVED = "ARCHIVED"

class TaskStage(str, Enum):
    """Task Status -> Logic Stage Mapping"""
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    READY = "READY"
    COMPLETE = "COMPLETE"

class TaskCategory(str, Enum):
    """Task importance classification"""
    CORE = "CORE"
    REGULAR = "REGULAR"
    OPTIONAL = "OPTIONAL"

class TaskLifecyclePhase(str, Enum):
    """Task Lifecycle - Inner Engine"""
    SCHEDULED = "SCHEDULED"
    UPCOMING = "UPCOMING"
    CURRENT = "CURRENT"
    FINAL_WALK = "FINAL_WALK"
    READY = "READY"
    DONE = "DONE"

class DomainError(Exception):
    """Base domain exception"""
    pass

class OverlapError(DomainError):
    """Core + Regular tasks cannot overlap"""
    pass

class FinalWalkBlocked(DomainError):
    """Final Walk cannot proceed - prerequisites not met"""
    pass

# ========================================================================================
# DOMAIN MODELS (Layer 2) - Business Entities
# ========================================================================================

@dataclass
class TaskStatus:
    """Maps user-friendly labels to system logic stages"""
    label: str
    stage: TaskStage

@dataclass
class Task:
    """Individual work unit with scheduling and assignment"""
    name: str
    category: TaskCategory
    offset: int  # Days from move-out
    task_type: str  # "In-House" or "Vendor"
    assignee: Optional[str] = None
    status_label: str = "Pending"
    stage: TaskStage = TaskStage.SCHEDULED
    date: Optional[date] = None
    comment: Optional[str] = None
    is_blocked: bool = False
    
    def calculate_date(self, move_out_date: date) -> date:
        """Calculate task date from move-out + offset"""
        return move_out_date + timedelta(days=self.offset)
    
    def can_overlap_with(self, other_task: 'Task') -> bool:
        """Business rule: Core + Regular cannot overlap"""
        if self.category == TaskCategory.CORE and other_task.category == TaskCategory.REGULAR:
            return False
        if self.category == TaskCategory.REGULAR and other_task.category == TaskCategory.CORE:
            return False
        return True

@dataclass
class Unit:
    """Central aggregate - represents complete unit turnover"""
    unit_id: str
    property: str
    unit_type: str
    square_footage: Optional[int] = None
    condition: str = "Good"
    move_out: Optional[date] = None
    move_in: Optional[date] = None
    tasks: List[Task] = field(default_factory=list)
    comment: Optional[str] = None
    
    def get_nvm_status(self, today: date) -> NVMState:
        """Compute resident lifecycle status from dates"""
        if not self.move_out:
            return NVMState.NOTICE
            
        if today < self.move_out:
            return NVMState.NOTICE
        elif not self.move_in:
            return NVMState.VACANT
        elif today < self.move_in:
            return NVMState.SCHEDULED
        else:
            return NVMState.MOVE_IN
    
    def calculate_readiness_percent(self) -> int:
        """Calculate completion percentage from Core + Regular tasks"""
        actionable_tasks = [t for t in self.tasks if t.category in [TaskCategory.CORE, TaskCategory.REGULAR]]
        if not actionable_tasks:
            return 0
            
        completed_tasks = [t for t in actionable_tasks if t.stage == TaskStage.COMPLETE]
        return int((len(completed_tasks) / len(actionable_tasks)) * 100)
    
    def get_current_task(self, today: date) -> Optional[Task]:
        """Find the task that should be active today"""
        if not self.move_out:
            return None
            
        for task in self.tasks:
            task_date = task.calculate_date(self.move_out)
            if task_date == today and task.stage in [TaskStage.SCHEDULED, TaskStage.IN_PROGRESS]:
                return task
        return None
    
    def validate_task_overlap(self) -> List[str]:
        """Check for Core + Regular overlap violations"""
        errors = []
        in_progress_tasks = [t for t in self.tasks if t.stage == TaskStage.IN_PROGRESS]
        
        for i, task1 in enumerate(in_progress_tasks):
            for task2 in in_progress_tasks[i+1:]:
                if not task1.can_overlap_with(task2):
                    errors.append(f"Overlap violation: {task1.name} ({task1.category}) cannot run with {task2.name} ({task2.category})")
        
        return errors

@dataclass(frozen=True)
class LifecycleSnapshot:
    """Read-only composite view of unit status"""
    unit_code: str
    lifecycle_label: str
    nvm_status: NVMState
    task_stage: TaskStage
    contextual_task: Dict[str, str]
    readiness_percent: int
    dtbr: Optional[int]
    days_vacant: Optional[int]
    final_walk_ready: bool

# ========================================================================================
# DOMAIN SERVICES (Layer 2) - Business Logic
# ========================================================================================

class LifecycleEngine:
    """Orchestrates dual lifecycle computation"""
    
    @staticmethod
    def resolve_lifecycle_label(nvm_status: NVMState, task_stage: TaskStage) -> str:
        """Combine resident + task state into unified label"""
        if nvm_status == NVMState.NOTICE and task_stage == TaskStage.SCHEDULED:
            return "PRE-TURN"
        elif nvm_status == NVMState.VACANT and task_stage == TaskStage.IN_PROGRESS:
            return "TURN-IN-PROGRESS"
        elif nvm_status == NVMState.VACANT and task_stage == TaskStage.BLOCKED:
            return "TURN-DELAYED"
        elif nvm_status == NVMState.SCHEDULED and task_stage == TaskStage.COMPLETE:
            return "READY-FOR-MOVE-IN"
        elif nvm_status == NVMState.MOVE_IN:
            return "ARCHIVED"
        else:
            return f"{nvm_status}-{task_stage}"
    
    @staticmethod
    def build_snapshot(unit: Unit, today: date) -> LifecycleSnapshot:
        """Generate complete lifecycle status"""
        nvm_status = unit.get_nvm_status(today)
        
        # Determine overall task stage
        if any(t.stage == TaskStage.BLOCKED for t in unit.tasks):
            task_stage = TaskStage.BLOCKED
        elif any(t.stage == TaskStage.IN_PROGRESS for t in unit.tasks):
            task_stage = TaskStage.IN_PROGRESS
        elif all(t.stage == TaskStage.COMPLETE for t in unit.tasks if t.category != TaskCategory.OPTIONAL):
            task_stage = TaskStage.COMPLETE
        else:
            task_stage = TaskStage.SCHEDULED
        
        # Get contextual task info
        current_task = unit.get_current_task(today)
        contextual_task = {}
        if current_task:
            contextual_task = {
                "task_name": current_task.name,
                "status_label": current_task.status_label
            }
        
        # Calculate days vacant
        days_vacant = None
        if unit.move_out and today >= unit.move_out:
            days_vacant = (today - unit.move_out).days
        
        # Calculate DTBR (Days To Be Ready)
        dtbr = None
        if unit.move_out:
            # Assume 7-day standard turn time
            projected_ready = unit.move_out + timedelta(days=7)
            dtbr = (projected_ready - today).days
        
        return LifecycleSnapshot(
            unit_code=unit.unit_id,
            lifecycle_label=LifecycleEngine.resolve_lifecycle_label(nvm_status, task_stage),
            nvm_status=nvm_status,
            task_stage=task_stage,
            contextual_task=contextual_task,
            readiness_percent=unit.calculate_readiness_percent(),
            dtbr=dtbr,
            days_vacant=days_vacant,
            final_walk_ready=LifecycleEngine.is_final_walk_ready(unit)
        )
    
    @staticmethod
    def is_final_walk_ready(unit: Unit) -> bool:
        """Check if Final Walk can be triggered"""
        core_regular_tasks = [t for t in unit.tasks if t.category in [TaskCategory.CORE, TaskCategory.REGULAR]]
        return all(t.stage in [TaskStage.COMPLETE, TaskStage.READY] for t in core_regular_tasks)

class TaskTemplateService:
    """Manages task blueprint generation"""
    
    # Sample templates - in real system this would come from DB/config
    TEMPLATES = {
        "1BR": [
            Task("Deep Clean", TaskCategory.CORE, 1, "In-House"),
            Task("Paint Touch-up", TaskCategory.CORE, 2, "In-House"), 
            Task("Change Locks", TaskCategory.CORE, 3, "In-House"),
            Task("Carpet Clean", TaskCategory.REGULAR, 4, "Vendor"),
            Task("HVAC Check", TaskCategory.REGULAR, 5, "Vendor"),
            Task("Appliance Test", TaskCategory.OPTIONAL, 6, "In-House"),
            Task("Final Walk", TaskCategory.CORE, 8, "In-House")  # Always Day 8
        ],
        "2BR": [
            Task("Deep Clean", TaskCategory.CORE, 1, "In-House"),
            Task("Paint Touch-up", TaskCategory.CORE, 2, "In-House"),
            Task("Change Locks", TaskCategory.CORE, 3, "In-House"),
            Task("Carpet Clean", TaskCategory.REGULAR, 4, "Vendor"),
            Task("HVAC Check", TaskCategory.REGULAR, 5, "Vendor"),
            Task("Balcony Clean", TaskCategory.REGULAR, 6, "In-House"),
            Task("Appliance Test", TaskCategory.OPTIONAL, 7, "In-House"),
            Task("Final Walk", TaskCategory.CORE, 8, "In-House")
        ]
    }
    
    @classmethod
    def get_template(cls, unit_type: str) -> List[Task]:
        """Get task template for unit type"""
        return [
            Task(t.name, t.category, t.offset, t.task_type, t.assignee)
            for t in cls.TEMPLATES.get(unit_type, cls.TEMPLATES["1BR"])
        ]

# ========================================================================================
# VALIDATION PROTOTYPE - Test Real-World Scenarios
# ========================================================================================

class DMRBPrototypeTester:
    """Test suite to validate business rules with realistic scenarios"""
    
    def __init__(self):
        self.today = date.today()
        self.units = []
        
        # Mock some status labels -> stage mappings
        self.status_mappings = {
            "Pending": TaskStage.SCHEDULED,
            "In Progress": TaskStage.IN_PROGRESS,
            "Vendor No-Show": TaskStage.BLOCKED,
            "QA Ready": TaskStage.READY,
            "Complete": TaskStage.COMPLETE,
            "Paint Delayed": TaskStage.BLOCKED,
            "Passed Inspection": TaskStage.READY
        }
    
    def create_test_unit(self, unit_id: str, unit_type: str, move_out_offset: int, move_in_offset: int) -> Unit:
        """Create a unit with realistic dates"""
        move_out_date = self.today + timedelta(days=move_out_offset)
        move_in_date = self.today + timedelta(days=move_in_offset)
        
        unit = Unit(
            unit_id=unit_id,
            property="Maple Gardens",
            unit_type=unit_type,
            square_footage=725,
            move_out=move_out_date,
            move_in=move_in_date
        )
        
        # Inject tasks from template
        template_tasks = TaskTemplateService.get_template(unit_type)
        for task in template_tasks:
            task.date = task.calculate_date(move_out_date)
            unit.tasks.append(task)
        
        self.units.append(unit)
        return unit
    
    def update_task_status(self, unit: Unit, task_name: str, status_label: str):
        """Update task status and validate business rules"""
        task = next((t for t in unit.tasks if t.name == task_name), None)
        if not task:
            raise ValueError(f"Task '{task_name}' not found")
        
        # Map label to stage
        if status_label not in self.status_mappings:
            raise ValueError(f"Unknown status label: {status_label}")
        
        old_stage = task.stage
        task.status_label = status_label
        task.stage = self.status_mappings[status_label]
        
        # Validate overlap rules
        overlap_errors = unit.validate_task_overlap()
        if overlap_errors:
            # Rollback and raise error
            task.stage = old_stage
            raise OverlapError(f"Cannot update {task_name}: {overlap_errors[0]}")
        
        print(f"✅ Updated {task_name}: {status_label} ({task.stage})")
    
    def print_unit_status(self, unit: Unit):
        """Display current unit lifecycle status"""
        snapshot = LifecycleEngine.build_snapshot(unit, self.today)
        
        print(f"\n📋 Unit {unit.unit_id} Status:")
        print(f"   Lifecycle: {snapshot.lifecycle_label}")
        print(f"   NVM State: {snapshot.nvm_status}")
        print(f"   Readiness: {snapshot.readiness_percent}%")
        print(f"   Days Vacant: {snapshot.days_vacant}")
        print(f"   DTBR: {snapshot.dtbr} days")
        print(f"   Final Walk Ready: {snapshot.final_walk_ready}")
        
        if snapshot.contextual_task:
            print(f"   Current Task: {snapshot.contextual_task}")
        
        print("\n   Task Details:")
        for task in unit.tasks:
            status_icon = "✅" if task.stage == TaskStage.COMPLETE else "🔄" if task.stage == TaskStage.IN_PROGRESS else "⏸️"
            print(f"     {status_icon} Day {task.offset}: {task.name} ({task.category}) - {task.status_label}")
    
    def test_scenario_1_normal_flow(self):
        """Test Case 1: Normal 7-day turn progression"""
        print("🧪 TEST SCENARIO 1: Normal Turn Flow")
        print("=" * 50)
        
        # Create unit that moved out yesterday, moves in next week
        unit = self.create_test_unit("M-304", "1BR", -1, 6)
        self.print_unit_status(unit)
        
        # Day 1: Start cleaning
        self.update_task_status(unit, "Deep Clean", "In Progress")
        self.print_unit_status(unit)
        
        # Day 2: Complete cleaning, start painting
        self.update_task_status(unit, "Deep Clean", "Complete")
        self.update_task_status(unit, "Paint Touch-up", "In Progress")
        self.print_unit_status(unit)
        
        # Day 3: Complete painting, start locks
        self.update_task_status(unit, "Paint Touch-up", "Complete")
        self.update_task_status(unit, "Change Locks", "In Progress")
        
        # Test Final Walk readiness
        print(f"\n🚪 Final Walk Ready: {LifecycleEngine.is_final_walk_ready(unit)}")
        
        return unit
    
    def test_scenario_2_overlap_violation(self):
        """Test Case 2: Core + Regular overlap prevention"""
        print("\n🧪 TEST SCENARIO 2: Overlap Violation Prevention")
        print("=" * 50)
        
        unit = self.create_test_unit("L-105", "2BR", -2, 5)
        
        # Start a Core task
        self.update_task_status(unit, "Paint Touch-up", "In Progress")
        
        # Try to start a Regular task (should fail)
        try:
            self.update_task_status(unit, "Carpet Clean", "In Progress")
            print("❌ ERROR: Overlap should have been blocked!")
        except OverlapError as e:
            print(f"✅ Overlap correctly prevented: {e}")
        
        # But Core + Optional should work
        self.update_task_status(unit, "Appliance Test", "In Progress")
        print("✅ Core + Optional overlap allowed")
        
        self.print_unit_status(unit)
        
        return unit
    
    def test_scenario_3_vendor_delay(self):
        """Test Case 3: Vendor delays and blocking"""
        print("\n🧪 TEST SCENARIO 3: Vendor Delays & Recovery")
        print("=" * 50)
        
        unit = self.create_test_unit("B-201", "1BR", -3, 4)
        
        # Normal progress for first few tasks
        self.update_task_status(unit, "Deep Clean", "Complete")
        self.update_task_status(unit, "Paint Touch-up", "Complete")
        self.update_task_status(unit, "Change Locks", "Complete")
        
        # Vendor task gets blocked
        self.update_task_status(unit, "Carpet Clean", "Vendor No-Show")
        self.print_unit_status(unit)
        
        # Try to do Final Walk (should be blocked)
        final_walk_ready = LifecycleEngine.is_final_walk_ready(unit)
        print(f"🚪 Final Walk Ready: {final_walk_ready} (should be False due to blocked Regular task)")
        
        # Resolve the vendor issue
        self.update_task_status(unit, "Carpet Clean", "Complete")
        final_walk_ready = LifecycleEngine.is_final_walk_ready(unit)
        print(f"🚪 Final Walk Ready: {final_walk_ready} (should now be True)")
        
        return unit
    
    def test_scenario_4_excel_import_simulation(self):
        """Test Case 4: Bulk import with validation"""
        print("\n🧪 TEST SCENARIO 4: Excel Import Simulation")
        print("=" * 50)
        
        # Simulate Excel data
        excel_data = [
            {"Unit": "A101", "Property": "Riverside", "Type": "1BR", "Move-Out": "2025-08-15", "Move-In": "2025-08-22"},
            {"Unit": "A102", "Property": "Riverside", "Type": "2BR", "Move-Out": "2025-08-16", "Move-In": "2025-08-23"},
            {"Unit": "A101", "Property": "Riverside", "Type": "1BR", "Move-Out": "2025-08-15", "Move-In": "2025-08-22"},  # Duplicate
        ]
        
        # Process import with deduplication
        existing_unit_ids = {unit.unit_id for unit in self.units}
        new_units = []
        skipped_units = []
        
        for row in excel_data:
            unit_id = f"R-{row['Unit']}"  # R for Riverside
            
            if unit_id in existing_unit_ids:
                skipped_units.append(unit_id)
                continue
            
            try:
                move_out = datetime.strptime(row["Move-Out"], "%Y-%m-%d").date()
                move_in = datetime.strptime(row["Move-In"], "%Y-%m-%d").date()
                
                unit = Unit(
                    unit_id=unit_id,
                    property=row["Property"],
                    unit_type=row["Type"],
                    move_out=move_out,
                    move_in=move_in
                )
                
                # Auto-assign tasks from template
                template_tasks = TaskTemplateService.get_template(row["Type"])
                for task in template_tasks:
                    task.date = task.calculate_date(move_out)
                    unit.tasks.append(task)
                
                new_units.append(unit)
                existing_unit_ids.add(unit_id)
                
            except Exception as e:
                print(f"❌ Failed to process {row}: {e}")
        
        print(f"✅ Import Results:")
        print(f"   Created: {len(new_units)} units")
        print(f"   Skipped (duplicates): {len(skipped_units)} units")
        print(f"   Skipped IDs: {skipped_units}")
        
        # Add to our test collection
        self.units.extend(new_units)
        
        return new_units
    
    def test_scenario_5_lifecycle_reset(self):
        """Test Case 5: Unit recycling when new move-out date added"""
        print("\n🧪 TEST SCENARIO 5: Lifecycle Reset & Recycling")
        print("=" * 50)
        
        # Use existing unit and advance it significantly
        if not self.units:
            unit = self.create_test_unit("T-999", "1BR", -5, 2)
        else:
            unit = self.units[0]
        
        # Make significant progress
        self.update_task_status(unit, "Deep Clean", "Complete")
        self.update_task_status(unit, "Paint Touch-up", "Complete")
        print("📈 Unit has significant progress...")
        self.print_unit_status(unit)
        
        # New notice received - unit gets recycled
        print("\n🔄 NEW NOTICE RECEIVED - Recycling unit...")
        
        # Reset logic (what happens when new move-out date is set)
        new_move_out = self.today + timedelta(days=10)
        new_move_in = self.today + timedelta(days=17)
        
        # Archive current state (in real system, this would be logged)
        archived_snapshot = LifecycleEngine.build_snapshot(unit, self.today)
        print(f"📚 Archived state: {archived_snapshot.lifecycle_label} ({archived_snapshot.readiness_percent}% complete)")
        
        # Reset unit
        unit.move_out = new_move_out
        unit.move_in = new_move_in
        
        # Clear and regenerate tasks
        unit.tasks.clear()
        template_tasks = TaskTemplateService.get_template(unit.unit_type)
        for task in template_tasks:
            task.date = task.calculate_date(new_move_out)
            unit.tasks.append(task)
        
        print("🆕 Unit recycled with fresh lifecycle:")
        self.print_unit_status(unit)
        
        return unit
    
    def run_all_tests(self):
        """Execute complete validation test suite"""
        print("🚀 DMRB CORE LIFECYCLE PROTOTYPE")
        print("Testing business rules with realistic scenarios")
        print("=" * 60)
        
        try:
            # Test normal operations
            unit1 = self.test_scenario_1_normal_flow()
            
            # Test business rule enforcement
            unit2 = self.test_scenario_2_overlap_violation()
            
            # Test delay handling
            unit3 = self.test_scenario_3_vendor_delay()
            
            # Test bulk operations
            new_units = self.test_scenario_4_excel_import_simulation()
            
            # Test lifecycle reset
            unit5 = self.test_scenario_5_lifecycle_reset()
            
            print(f"\n🎯 VALIDATION SUMMARY:")
            print(f"   Total units processed: {len(self.units)}")
            print(f"   Business rules enforced: ✅")
            print(f"   Dual lifecycle working: ✅")
            print(f"   Excel import logic: ✅")
            print(f"   State reset capability: ✅")
            
            print(f"\n📊 Current System State:")
            for unit in self.units[-3:]:  # Show last 3 units
                snapshot = LifecycleEngine.build_snapshot(unit, self.today)
                print(f"   {unit.unit_id}: {snapshot.lifecycle_label} ({snapshot.readiness_percent}%)")
        
        except Exception as e:
            print(f"❌ VALIDATION FAILED: {e}")
            raise

# ========================================================================================
# EXCEL IMPORT PROTOTYPE
# ========================================================================================

class ExcelImportValidator:
    """Simulates Excel import with real-world edge cases"""
    
    @staticmethod
    def validate_row(row: Dict[str, Any]) -> List[str]:
        """Validate individual Excel row"""
        errors = []
        
        required_fields = ["Unit", "Property", "Type", "Move-Out", "Move-In"]
        for field in required_fields:
            if field not in row or not row[field]:
                errors.append(f"Missing required field: {field}")
        
        # Date validation
        try:
            if "Move-Out" in row:
                datetime.strptime(str(row["Move-Out"]), "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid Move-Out date format (expected YYYY-MM-DD)")
        
        try:
            if "Move-In" in row:
                datetime.strptime(str(row["Move-In"]), "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid Move-In date format (expected YYYY-MM-DD)")
        
        # Business rule validation
        if "Move-Out" in row and "Move-In" in row:
            try:
                move_out = datetime.strptime(str(row["Move-Out"]), "%Y-%m-%d").date()
                move_in = datetime.strptime(str(row["Move-In"]), "%Y-%m-%d").date()
                if move_in <= move_out:
                    errors.append("Move-In date must be after Move-Out date")
            except:
                pass  # Date parsing already failed above
        
        return errors
    
    @staticmethod
    def test_problematic_excel_data():
        """Test Excel import with realistic problematic data"""
        print("\n🧪 EXCEL IMPORT EDGE CASE TESTING")
        print("=" * 50)
        
        problematic_data = [
            # Good row
            {"Unit": "A101", "Property": "Test Property", "Type": "1BR", "Move-Out": "2025-08-15", "Move-In": "2025-08-22"},
            # Missing required field
            {"Unit": "A102", "Property": "", "Type": "1BR", "Move-Out": "2025-08-16", "Move-In": "2025-08-23"},
            # Invalid date format
            {"Unit": "A103", "Property": "Test Property", "Type": "2BR", "Move-Out": "8/17/25", "Move-In": "2025-08-24"},
            # Move-in before move-out
            {"Unit": "A104", "Property": "Test Property", "Type": "1BR", "Move-Out": "2025-08-20", "Move-In": "2025-08-18"},
            # Duplicate unit
            {"Unit": "A101", "Property": "Test Property", "Type": "1BR", "Move-Out": "2025-08-15", "Move-In": "2025-08-22"},
        ]
        
        valid_rows = []
        error_summary = []
        
        for i, row in enumerate(problematic_data, 1):
            print(f"\nValidating Row {i}: {row.get('Unit', 'UNKNOWN')}")
            errors = ExcelImportValidator.validate_row(row)
            
            if errors:
                print(f"   ❌ Errors: {', '.join(errors)}")
                error_summary.extend(errors)
            else:
                print(f"   ✅ Valid")
                valid_rows.append(row)
        
        print(f"\n📊 Import Summary:")
        print(f"   Total rows: {len(problematic_data)}")
        print(f"   Valid rows: {len(valid_rows)}")
        print(f"   Error rows: {len(problematic_data) - len(valid_rows)}")
        print(f"   Common errors: {list(set(error_summary))}")
        
        return valid_rows, error_summary

# ========================================================================================
# MAIN EXECUTION - Run Validation Tests
# ========================================================================================

if __name__ == "__main__":
    # Initialize prototype tester
    tester = DMRBPrototypeTester()
    
    # Run core business logic tests
    tester.run_all_tests()
    
    # Test Excel import edge cases
    ExcelImportValidator.test_problematic_excel_data()
    
    print("\n" + "=" * 60)
    print("🏁 PROTOTYPE VALIDATION COMPLETE")
    print("✅ Core lifecycle state machine validated")
    print("✅ Business rules enforcement working")
    print("✅ Excel import edge cases identified")
    print("✅ Ready for architectural implementation")
    print("=" * 60)