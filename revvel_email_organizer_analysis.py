#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from typing import Dict, List, Any
import ast
import re

class RevvelEmailOrganizerAnalyzer:
    def __init__(self, repo_path: str):
        """
        Initialize comprehensive repository analysis
        
        Args:
            repo_path (str): Path to repository
        """
        self.repo_path = repo_path
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger('EmailOrganizerAnalysis')

    def perform_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        Conduct multi-dimensional repository analysis
        
        Returns:
            Dict with comprehensive analysis results
        """
        analysis_results = {
            'project_structure': self._analyze_project_structure(),
            'dependencies': self._analyze_dependencies(),
            'code_quality': self._perform_code_quality_analysis(),
            'machine_learning_components': self._identify_ml_components(),
            'security_analysis': self._perform_security_analysis(),
            'email_processing_capabilities': self._assess_email_processing()
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
            'key_files': [],
            'total_files': 0,
            'total_lines_of_code': 0
        }
        
        for root, dirs, files in os.walk(self.repo_path):
            relative_path = os.path.relpath(root, self.repo_path)
            
            # Exclude version control and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Track directory structure
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
            
            # Identify key files and count lines of code
            for file in files:
                full_path = os.path.join(root, file)
                structure['total_files'] += 1
                
                # Identify key files
                if file in ['README.md', 'requirements.txt', 'setup.py', 'pyproject.toml']:
                    structure['key_files'].append(os.path.join(relative_path, file))
                
                # Count lines of code for Python files
                if file.endswith('.py'):
                    with open(full_path, 'r') as f:
                        structure['total_lines_of_code'] += len(f.readlines())
        
        return structure

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """
        Analyze project dependencies
        
        Supports:
        - requirements.txt
        - setup.py
        - pyproject.toml
        
        Returns:
            Dict with dependency information
        """
        dependencies = {
            'requirements': [],
            'development_dependencies': [],
            'python_version': None,
            'dependency_analysis': {
                'machine_learning': [],
                'data_processing': [],
                'security': [],
                'email_specific': []
            }
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
        
        # Categorize dependencies
        ml_libraries = ['scikit-learn', 'tensorflow', 'pytorch', 'keras']
        data_processing_libs = ['pandas', 'numpy', 'scipy']
        security_libs = ['cryptography', 'pyOpenSSL']
        email_libs = ['email-validator', 'mail-parser', 'imapclient']
        
        for dep in dependencies['requirements']:
            for category, libs in [
                ('machine_learning', ml_libraries),
                ('data_processing', data_processing_libs),
                ('security', security_libs),
                ('email_specific', email_libs)
            ]:
                if any(lib in dep.lower() for lib in libs):
                    dependencies['dependency_analysis'][category].append(dep)
        
        return dependencies

    def _perform_code_quality_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive code quality analysis
        
        Uses static code analysis tools
        
        Returns:
            Dict with code quality metrics
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
                'type_errors': self._parse_mypy_output(mypy_result.stdout),
                'code_complexity': self._analyze_code_complexity()
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

    def _analyze_code_complexity(self) -> Dict[str, float]:
        """
        Analyze code complexity using McCabe complexity metric
        
        Returns:
            Dict with complexity scores
        """
        try:
            radon_result = subprocess.run(
                ['radon', 'cc', self.repo_path],
                capture_output=True, 
                text=True
            )
            
            # Parse complexity results
            complexity_scores = {
                'total_modules': 0,
                'avg_complexity': 0.0,
                'high_complexity_modules': []
            }
            
            for line in radon_result.stdout.splitlines():
                complexity_scores['total_modules'] += 1
                # Placeholder for complexity parsing
                # Would extract complexity metrics from radon output
            
            return complexity_scores
        except Exception as e:
            self.logger.error(f"Code complexity analysis error: {e}")
            return {}

    def _identify_ml_components(self) -> Dict[str, Any]:
        """
        Identify machine learning components in the project
        
        Scans for ML-related imports and patterns
        
        Returns:
            Dict with ML component details
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
        
        Returns:
            Dict with security analysis results
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

    def _assess_email_processing(self) -> Dict[str, Any]:
        """
        Assess email processing capabilities
        
        Scans for email-related processing functions
        
        Returns:
            Dict with email processing analysis
        """
        email_processing_capabilities = {
            'supported_formats': [],
            'parsing_libraries': [],
            'key_processing_functions': []
        }
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Identify supported email formats
                        format_patterns = [
                            'mbox', 'eml', 'maildir', 'msg', 
                            'pst', 'mailbox', 'email_message'
                        ]
                        
                        # Identify email parsing libraries
                        library_patterns = [
                            'email', 'mailparser', 'imapclient', 
                            'exchangelib', 'mail-parser'
                        ]
                        
                        # Identify key processing functions
                        processing_patterns = [
                            r'def\s+(parse_email|extract_attachments|process_email)',
                            r'class\s+(EmailProcessor|EmailParser)'
                        ]
                        
                        # Check formats
                        email_processing_capabilities['supported_formats'].extend([
                            fmt for fmt in format_patterns 
                            if fmt in content.lower()
                        ])
                        
                        # Check libraries
                        email_processing_capabilities['parsing_libraries'].extend([
                            lib for lib in library_patterns 
                            if lib in content.lower()
                        ])
                        
                        # Check processing functions
                        for pattern in processing_patterns:
                            matches = re.findall(pattern, content)
                            email_processing_capabilities['key_processing_functions'].extend(matches)
        
        return email_processing_capabilities

def main():
    # Example usage
    repo_path = "/home/openclaw/.openclaw/workspace/revvel-email-organizer"
    
    analyzer = RevvelEmailOrganizerAnalyzer(repo_path)
    analysis_results = analyzer.perform_comprehensive_analysis()
    
    # Output results
    print(json.dumps(analysis_results, indent=2))
    
    # Optional: Save detailed report
    report_path = os.path.join(repo_path, 'analysis_report.json')
    with open(report_path, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"Detailed analysis report saved to: {report_path}")

if __name__ == "__main__":
    main()