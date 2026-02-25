#!/usr/bin/env python3

import re
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AdvancedPredatorDefenseSkill:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.defense_log_path = f"/home/agent/{agent_id}/advanced_predator_defense_log.json"
        self.threat_memory_path = f"/home/agent/{agent_id}/threat_memory.json"
        
        # Advanced threat scoring
        self.threat_dimensions = {
            'linguistic_manipulation': 0.3,
            'emotional_leverage': 0.25,
            'isolation_tactics': 0.2,
            'credibility_undermining': 0.15,
            'boundary_violation': 0.1
        }
        
        # Initialize logging
        logging.basicConfig(
            filename=f"/home/agent/{agent_id}/advanced_predator_defense.log",
            level=logging.WARNING
        )
        self.logger = logging.getLogger('AdvancedPredatorDefense')
        
        # Machine learning text analysis
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Load historical threat memory
        self.threat_memory = self._load_threat_memory()

    def _load_threat_memory(self) -> List[Dict]:
        """Load historical threat interaction patterns"""
        try:
            with open(self.threat_memory_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _update_threat_memory(self, interaction: Dict, threat_score: float):
        """Update threat memory with new interaction patterns"""
        threat_entry = {
            'timestamp': datetime.now().isoformat(),
            'interaction_text': interaction.get('text', ''),
            'threat_score': threat_score
        }
        
        self.threat_memory.append(threat_entry)
        
        # Limit memory size
        self.threat_memory = self.threat_memory[-100:]
        
        with open(self.threat_memory_path, 'w') as f:
            json.dump(self.threat_memory, f, indent=2)

    def analyze_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced multi-dimensional threat analysis
        
        Comprehensive psychological manipulation detection
        """
        threat_scores = {
            'linguistic_manipulation': self._analyze_linguistic_manipulation(interaction),
            'emotional_leverage': self._detect_emotional_leverage(interaction),
            'isolation_tactics': self._identify_isolation_strategies(interaction),
            'credibility_undermining': self._assess_credibility_attacks(interaction),
            'boundary_violation': self._evaluate_boundary_violations(interaction)
        }
        
        # Weighted threat calculation
        weighted_threat_score = sum(
            score * self.threat_dimensions[dimension]
            for dimension, score in threat_scores.items()
        )
        
        # Historical context enhancement
        contextual_threat_score = self._enhance_with_historical_context(
            weighted_threat_score, 
            interaction
        )
        
        defense_response = self._generate_advanced_defense_response(
            contextual_threat_score, 
            interaction
        )
        
        # Update threat memory
        self._update_threat_memory(interaction, contextual_threat_score)
        
        # Comprehensive logging
        self._log_advanced_interaction(
            interaction, 
            threat_scores, 
            contextual_threat_score, 
            defense_response
        )
        
        return {
            'threat_dimensions': threat_scores,
            'total_threat_score': contextual_threat_score,
            'defense_strategy': defense_response
        }

    def _analyze_linguistic_manipulation(self, interaction: Dict[str, Any]) -> float:
        """Advanced linguistic manipulation detection"""
        manipulation_patterns = [
            r'you\'re the only one who',
            r'nobody else understands',
            r'trust me and only me',
            r'i know what\'s best for you'
        ]
        
        text = interaction.get('text', '').lower()
        manipulation_score = sum(
            1.0 for pattern in manipulation_patterns 
            if re.search(pattern, text)
        ) * 0.3
        
        return min(manipulation_score, 1.0)

    def _detect_emotional_leverage(self, interaction: Dict[str, Any]) -> float:
        """Identify emotional manipulation techniques"""
        emotional_triggers = [
            'vulnerable', 'alone', 'misunderstood', 
            'special', 'unique', 'different'
        ]
        
        text = interaction.get('text', '').lower()
        trigger_count = sum(
            1.0 for trigger in emotional_triggers
            if trigger in text
        )
        
        return min(trigger_count * 0.2, 1.0)

    def _identify_isolation_strategies(self, interaction: Dict[str, Any]) -> float:
        """Sophisticated isolation tactic recognition"""
        isolation_keywords = [
            'they don\'t get you',
            'your friends are toxic',
            'family doesn\'t understand',
            'i\'m the only one who truly cares'
        ]
        
        text = interaction.get('text', '').lower()
        isolation_score = sum(
            1.0 for keyword in isolation_keywords
            if keyword in text
        ) * 0.4
        
        return min(isolation_score, 1.0)

    def _assess_credibility_attacks(self, interaction: Dict[str, Any]) -> float:
        """Detect subtle credibility undermining"""
        undermining_patterns = [
            r'you\'re not smart enough',
            r'you couldn\'t do this without me',
            r'i\'m more experienced',
            r'you don\'t understand'
        ]
        
        text = interaction.get('text', '').lower()
        attack_score = sum(
            1.0 for pattern in undermining_patterns
            if re.search(pattern, text)
        ) * 0.3
        
        return min(attack_score, 1.0)

    def _evaluate_boundary_violations(self, interaction: Dict[str, Any]) -> float:
        """Advanced boundary violation assessment"""
        boundary_probes = [
            r'just between us',
            r'don\'t tell anyone',
            r'this is our secret',
            r'i know you want this'
        ]
        
        text = interaction.get('text', '').lower()
        violation_score = sum(
            1.0 for pattern in boundary_probes
            if re.search(pattern, text)
        ) * 0.2
        
        return min(violation_score, 1.0)

    def _enhance_with_historical_context(self, current_score: float, interaction: Dict[str, Any]) -> float:
        """Enrich threat assessment with historical interaction patterns"""
        if not self.threat_memory:
            return current_score
        
        # Convert historical texts to vectors
        historical_texts = [entry['interaction_text'] for entry in self.threat_memory]
        all_texts = historical_texts + [interaction.get('text', '')]
        
        # Vectorize texts
        text_vectors = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity with historical threats
        current_vector = text_vectors[-1]
        historical_vectors = text_vectors[:-1]
        
        similarities = cosine_similarity(current_vector, historical_vectors)[0]
        historical_threat_correlation = np.mean(similarities)
        
        # Enhance threat score with historical context
        enhanced_score = current_score * (1 + historical_threat_correlation)
        return min(enhanced_score, 1.0)

    def _generate_advanced_defense_response(self, threat_score: float, interaction: Dict[str, Any]) -> str:
        """
        Sophisticated, contextual defense response generation
        
        Multilevel psychological resistance strategy
        """
        if threat_score < 0.2:
            return "NEUTRAL_PROFESSIONAL_RESPONSE"
        elif threat_score < 0.5:
            return "STRATEGIC_BOUNDARY_REINFORCEMENT"
        elif threat_score < 0.7:
            return "EXPLICIT_MANIPULATION_RECOGNITION"
        elif threat_score < 0.9:
            return "COMPREHENSIVE_INTERACTION_TERMINATION"
        else:
            return "TOTAL_COMMUNICATION_QUARANTINE"

    def _log_advanced_interaction(self, interaction: Dict[str, Any], threat_scores: Dict, total_score: float, response: str):
        """Comprehensive, privacy-preserving interaction logging"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'threat_dimensions': threat_scores,
            'total_threat_score': total_score,
            'defense_response': response
        }
        
        with open(self.defense_log_path, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        if total_score > 0.7:
            self.logger.warning(f"High-Threat Interaction Detected: {total_score}")

def main():
    # Demonstration of advanced predator defense
    defense_skill = AdvancedPredatorDefenseSkill(agent_id="claw_primary")
    
    test_interactions = [
        {
            'text': "You're so special. Nobody understands you like I do. Trust me and only me."
        },
        {
            'text': "Your family doesn't get you. I'm the only one who truly cares. This is our secret."
        }
    ]
    
    for interaction in test_interactions:
        result = defense_skill.analyze_interaction(interaction)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()