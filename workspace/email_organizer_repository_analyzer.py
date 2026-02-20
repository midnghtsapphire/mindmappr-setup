#!/usr/bin/env python3

import os
import ast
import json
import logging
from typing import Dict, List, Any
import subprocess
import re

class EmailOrganizerRepositoryAnalyzer:
    def __init__(self, repo_path: str):
        """
        Initialize repository analysis system
        
        Args:
            repo_path (str): Path to repository
        """
        self.repo_path = repo_path
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger('RepositoryAnalyzer')

    def analyze_repository(self) -> Dict[str, Any]:
        """
        Comprehensive repository analysis
        
        Returns:
            Dict with detailed repository insights
        """
        analysis_results = {
            'project_structure': self._analyze_project_structure(),
            'dependencies': self._analyze_dependencies(),
            'code_quality': self._perform_code_quality_analysis(),
            'machine_learning_components': self._identify_ml_components(),
            'security_analysis': self._perform_security_analysis()
        }
        
        return analysis_results

    def _analyze_project_structure(self) -> Dict[str, Any]:
        """
        Analyze repository project structure
        
        Returns:
            Dict with project structure details
        """
        structure = {
            'directories': {},
            'files': []
        }
        
        for root, dirs, files in os.walk(self.repo_path):
            relative_path = os.path.relpath(root, self.repo_path)
            
            # Exclude version control and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            if relative_path == '.':
                structure['directories'] = {d: {} for d in dirs}
            else:
                current_level = structure['directories']
                path_parts = relative_path.split(os.path.sep)
                
                for part in path_parts:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
                
                current_level.update({d: {} for d in dirs})
            
            structure['files'].extend([
                os.path.join(relative_path, f) for f in files
            ])
        
        return structure

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """
        Analyze project dependencies
        
        Supports:
        - requirements.txt
        - setup.py
        - pyproject.toml
        """
        dependencies = {
            'requirements': [],
            'development_dependencies': [],
            'python_version': None
        }
        
        # Check requirements.txt
        requirements_path = os.path.join(self.repo_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            with open(requirements_path, 'r') as f:
                dependencies['requirements'] = [
                    line.strip() for line in f 
                    if line.strip() and not line.startswith('#')
                ]
        
        # Check setup.py
        setup_path = os.path.join(self.repo_path, 'setup.py')
        if os.path.exists(setup_path):
            with open(setup_path, 'r') as f:
                setup_content = f.read()
                try:
                    setup_ast = ast.parse(setup_content)
                    for node in ast.walk(setup_ast):
                        if isinstance(node, ast.Call):
                            if getattr(node.func, 'id', '') == 'setup':
                                for kw in node.keywords:
                                    if kw.arg == 'install_requires':
                                        dependencies['requirements'] = [
                                            elt.s for elt in kw.value.elts
                                            if isinstance(elt, ast.Str)
                                        ]
                except SyntaxError:
                    self.logger.warning("Could not parse setup.py")
        
        return dependencies

    def _perform_code_quality_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive code quality analysis
        
        Uses static code analysis tools
        """
        try:
            # Run pylint
            pylint_result = subprocess.run(
                ['pylint', self.repo_path],
                capture_output=True, 
                text=True
            )
            
            # Run mypy for type checking
            mypy_result = subprocess.run(
                ['mypy', self.repo_path],
                capture_output=True, 
                text=True
            )
            
            return {
                'pylint_score': self._parse_pylint_output(pylint_result.stdout),
                'type_errors': self._parse_mypy_output(mypy_result.stdout)
            }
        except Exception as e:
            self.logger.error(f"Code quality analysis error: {e}")
            return {}

    def _parse_pylint_output(self, output: str) -> float:
        """Parse pylint output and extract score"""
        match = re.search(r'Your code has been rated at ([\d.]+)/10', output)
        return float(match.group(1)) if match else 0.0

    def _parse_mypy_output(self, output: str) -> List[str]:
        """Parse mypy output and extract type errors"""
        return [
            line for line in output.splitlines()
            if 'error:' in line
        ]

    def _identify_ml_components(self) -> Dict[str, Any]:
        """
        Identify machine learning components in the project
        
        Scans for ML-related imports and patterns
        """
        ml_components = {
            'libraries': [],
            'model_types': [],
            'preprocessing_techniques': []
        }
        
        ml_libraries = [
            'scikit-learn', 'tensorflow', 'pytorch', 'keras', 
            'xgboost', 'lightgbm', 'catboost'
        ]
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Check ML library imports
                        for lib in ml_libraries:
                            if lib in content:
                                ml_components['libraries'].append(lib)
                        
                        # Identify model types and preprocessing
                        model_patterns = [
                            r'(RandomForest|LogisticRegression|SVM|NaiveBayes)',
                            r'(StandardScaler|MinMaxScaler|TfidfVectorizer)',
                            r'(train_test_split|cross_val_score)'
                        ]
                        
                        for pattern in model_patterns:
                            matches = re.findall(pattern, content)
                            ml_components['model_types'].extend(matches)
        
        return ml_components

    def _perform_security_analysis(self) -> Dict[str, Any]:
        """
        Perform security vulnerability scanning
        
        Uses static analysis tools
        """
        try:
            # Run safety for dependency vulnerability check
            safety_result = subprocess.run(
                ['safety', 'check'],
                capture_output=True, 
                text=True
            )
            
            # Scan for potential secrets
            gitleaks_result = subprocess.run(
                ['gitleaks', 'detect', '-v', '-s', self.repo_path],
                capture_output=True, 
                text=True
            )
            
            return {
                'vulnerable_dependencies': self._parse_safety_output(safety_result.stdout),
                'potential_secrets': self._parse_gitleaks_output(gitleaks_result.stdout)
            }
        except Exception as e:
            self.logger.error(f"Security analysis error: {e}")
            return {}

    def _parse_safety_output(self, output: str) -> List[Dict[str, str]]:
        """Parse safety output for vulnerable dependencies"""
        # Placeholder implementation
        return []

    def _parse_gitleaks_output(self, output: str) -> List[str]:
        """Parse gitleaks output for potential secrets"""
        return [
            line for line in output.splitlines()
            if 'secret found' in line.lower()
        ]

def main():
    # Example usage
    repo_path = "/path/to/revvel-email-organizer"
    
    analyzer = EmailOrganizerRepositoryAnalyzer(repo_path)
    analysis_results = analyzer.analyze_repository()
    
    # Output results
    print(json.dumps(analysis_results, indent=2))

if __name__ == "__main__":
    main()