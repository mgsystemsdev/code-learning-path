# app/services/language_service.py
"""
Language Service - Business logic for language packs and suggestions.

Handles:
- Language pack loading and management
- Topic and skill suggestions
- Auto-fill logic based on text analysis
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple, Optional

from app.db import get_languages, load_language_pack


class LanguageService:
    """Service for managing language packs and providing smart suggestions."""

    def __init__(self):
        self.current_language_pack: Dict[str, Any] = {}

    def get_languages(self) -> List[Tuple[str, str, str]]:
        """Get list of available languages."""
        try:
            return get_languages() or []
        except Exception as e:
            raise Exception(f"Failed to get languages: {e}")

    def load_language_pack(self, language_code: str):
        """Load language pack for the specified language."""
        try:
            self.current_language_pack = load_language_pack(language_code) or {}
        except Exception as e:
            raise Exception(f"Failed to load language pack for {language_code}: {e}")

    def get_topics(self) -> List[str]:
        """Get list of topics for the current language pack."""
        return list(self.current_language_pack.get("topics", {}).keys())

    def get_skills(self) -> List[str]:
        """Get list of skills for the current language pack."""
        return list(self.current_language_pack.get("skills", {}).keys())

    def get_suggestions_from_text(self, text: str) -> Dict[str, str]:
        """
        Analyze text and return suggestions for topic and difficulty.
        
        Args:
            text: Combined text from work item name and notes
            
        Returns:
            Dictionary with 'topic' and 'difficulty' suggestions
        """
        if not text.strip():
            return {}

        try:
            text_lower = text.lower()
            best_topic = ""
            best_difficulty = ""
            best_score = 0

            # Analyze topics
            for topic, topic_info in self.current_language_pack.get("topics", {}).items():
                score = self._calculate_topic_score(topic, topic_info, text_lower)
                if score > best_score:
                    best_score = score
                    best_topic = topic
                    best_difficulty = topic_info.get("default_difficulty", "Beginner")

            # Analyze skills (can override topic-based difficulty)
            for skill_name, skill_info in self.current_language_pack.get("skills", {}).items():
                score = self._calculate_skill_score(skill_name, skill_info, text_lower)
                if score > best_score:
                    best_score = score
                    best_difficulty = skill_info.get("difficulty", best_difficulty)

            result = {}
            if best_topic and best_score > 0:
                result["topic"] = best_topic
            if best_difficulty and best_score > 0:
                result["difficulty"] = best_difficulty

            return result

        except Exception as e:
            print(f"Warning: Text analysis failed: {e}")
            return {}

    def _calculate_topic_score(self, topic: str, topic_info: Dict[str, Any], text: str) -> int:
        """Calculate relevance score for a topic based on text content."""
        score = 0
        
        # Direct topic name match
        if topic.lower() in text:
            score += 10
        
        # Check for topic keywords if available
        keywords = topic_info.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in text:
                score += 5
        
        # Check for topic aliases if available
        aliases = topic_info.get("aliases", [])
        for alias in aliases:
            if alias.lower() in text:
                score += 8
        
        return score

    def _calculate_skill_score(self, skill_name: str, skill_info: Dict[str, Any], text: str) -> int:
        """Calculate relevance score for a skill based on text content."""
        score = 0
        
        # Direct skill name match
        if skill_name.lower() in text:
            score += 15
        
        # Check for skill keywords
        keywords = skill_info.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in text:
                score += 5
        
        # Check for skill patterns if available
        patterns = skill_info.get("patterns", [])
        for pattern in patterns:
            if pattern.lower() in text:
                score += 7
        
        return score

    def get_topic_info(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific topic."""
        return self.current_language_pack.get("topics", {}).get(topic)

    def get_skill_info(self, skill: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific skill."""
        return self.current_language_pack.get("skills", {}).get(skill)

    def get_default_difficulty_for_topic(self, topic: str) -> str:
        """Get the default difficulty level for a topic."""
        topic_info = self.get_topic_info(topic)
        return topic_info.get("default_difficulty", "Beginner") if topic_info else "Beginner"

    def get_related_topics(self, topic: str) -> List[str]:
        """Get topics related to the specified topic."""
        topic_info = self.get_topic_info(topic)
        return topic_info.get("related_topics", []) if topic_info else []

    def get_prerequisites(self, topic: str) -> List[str]:
        """Get prerequisites for a topic."""
        topic_info = self.get_topic_info(topic)
        return topic_info.get("prerequisites", []) if topic_info else []

    def validate_difficulty_for_topic(self, topic: str, difficulty: str) -> bool:
        """Check if a difficulty level is appropriate for a topic."""
        topic_info = self.get_topic_info(topic)
        if not topic_info:
            return True  # Allow any difficulty if topic not found
        
        allowed_difficulties = topic_info.get("allowed_difficulties", [])
        if not allowed_difficulties:
            return True  # Allow any difficulty if not restricted
        
        return difficulty in allowed_difficulties

    def get_language_pack_info(self) -> Dict[str, Any]:
        """Get general information about the current language pack."""
        return {
            "name": self.current_language_pack.get("name", "Unknown"),
            "version": self.current_language_pack.get("version", "1.0"),
            "description": self.current_language_pack.get("description", ""),
            "topic_count": len(self.current_language_pack.get("topics", {})),
            "skill_count": len(self.current_language_pack.get("skills", {})),
        }