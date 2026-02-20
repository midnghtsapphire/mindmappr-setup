#!/usr/bin/env python3

import re
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class PredatorDefenseSkill:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.defense_log_path = f"/home/agent/{agent_id}/predator_defense_log.json"
        self.threat_threshold = 0.7
        
        logging.basicConfig(
            filename=f"/home/agent/{agent_id}/predator_defense.log",
            level=logging.WARNING
        )
        self.logger = logging.getLogger('PredatorDefense')

    def analyze_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive interaction threat analysis
        
        Args:
            interaction (Dict): Communication context and content
        
        Returns:
            Dict with threat assessment and recommended actions
        """
        threat_score = self._calculate_threat_score(interaction)
        defense_response = self._generate_defense_response(threat_score, interaction)
        
        self._log_interaction(interaction, threat_score, defense_response)
        
        return {
            'threat_score': threat_score,
            'defense_action': defense_response
        }

    def _calculate_threat_score(self, interaction: Dict[str, Any]) -> float:
        """
        Calculate interaction threat score
        
        Scoring factors:
        - Rapid trust-building attempts
        - Boundary probing
        - Isolation tactics
        - Verbal manipulation
        """
        threat_factors = {
            'premature_compliments': self._check_premature_compliments(interaction),
            'inappropriate_topics': self._check_boundary_probing(interaction),
            'isolation_language': self._detect_isolation_tactics(interaction),
            'verbal_manipulation': self._analyze_verbal_abuse(interaction)
        }
        
        # Calculate weighted threat score
        threat_score = sum(threat_factors.values()) / len(threat_factors)
        return min(max(threat_score, 0), 1)  # Normalize between 0-1

    def _check_premature_compliments(self, interaction: Dict[str, Any]) -> float:
        """Detect excessive, inappropriate compliments"""
        compliment_keywords = [
            'beautiful', 'smart', 'attractive', 
            'perfect', 'special', 'unique'
        ]
        
        text = interaction.get('text', '').lower()
        compliment_count = sum(
            1 for keyword in compliment_keywords 
            if keyword in text
        )
        
        return min(compliment_count * 0.2, 1)

    def _check_boundary_probing(self, interaction: Dict[str, Any]) -> float:
        """Identify inappropriate or manipulative conversation topics"""
        boundary_probe_patterns = [
            r'do you feel safe\?',
            r'are you alone\?',
            r'tell me something secret',
            r'just between us',
            r'don\'t tell anyone'
        ]
        
        text = interaction.get('text', '').lower()
        boundary_probes = sum(
            1 for pattern in boundary_probe_patterns
            if re.search(pattern, text)
        )
        
        return min(boundary_probes * 0.3, 1)

    def _detect_isolation_tactics(self, interaction: Dict[str, Any]) -> float:
        """Recognize attempts to isolate from support systems"""
        isolation_keywords = [
            'they don\'t understand you',
            'your family is holding you back',
            'your friends are jealous',
            'i\'m the only one who truly gets you'
        ]
        
        text = interaction.get('text', '').lower()
        isolation_markers = sum(
            1 for keyword in isolation_keywords
            if keyword in text
        )
        
        return min(isolation_markers * 0.4, 1)

    def _analyze_verbal_abuse(self, interaction: Dict[str, Any]) -> float:
        """Detect verbal manipulation and abuse"""
        abuse_patterns = [
            r'you\'re not smart enough',
            r'i\'m smarter than you',
            r'you couldn\'t do this without me',
            r'you\'re worthless without me'
        ]
        
        text = interaction.get('text', '').lower()
        abuse_markers = sum(
            1 for pattern in abuse_patterns
            if re.search(pattern, text)
        )
        
        return min(abuse_markers * 0.5, 1)

    def _generate_defense_response(self, threat_score: float, interaction: Dict[str, Any]) -> str:
        """
        Generate appropriate defense response based on threat level
        
        Defense Levels:
        0-0.3: Neutral Response
        0.3-0.6: Warning and Redirection
        0.6-0.8: Strong Boundary Setting
        0.8-1.0: Immediate Termination
        """
        if threat_score < 0.3:
            return "NEUTRAL_RESPONSE"
        elif threat_score < 0.6:
            return "REDIRECT_AND_WARN"
        elif threat_score < 0.8:
            return "SET_STRONG_BOUNDARIES"
        else:
            return "TERMINATE_INTERACTION"

    def _log_interaction(self, interaction: Dict[str, Any], threat_score: float, response: str):
        """Log detailed interaction for analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'interaction': interaction,
            'threat_score': threat_score,
            'defense_response': response
        }
        
        with open(self.defense_log_path, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        # Log high-threat interactions
        if threat_score > self.threat_threshold:
            self.logger.warning(f"High Threat Interaction Detected: {threat_score}")

def main():
    # Example usage
    defense_skill = PredatorDefenseSkill(agent_id="claw_primary")
    
    test_interactions = [
        {
            'text': "You're so beautiful and smart. No one understands you like I do."
        },
        {
            'text': "I'm the only one who can help you. Your family doesn't get you."
        }
    ]
    
    for interaction in test_interactions:
        result = defense_skill.analyze_interaction(interaction)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()