#!/usr/bin/env python3

import os
import json
import subprocess
import pdoc
import markdown2
import shutil

class DocumentationGenerator:
    def __init__(self, project_root: str):
        """
        Initialize documentation generation system
        
        Args:
            project_root (str): Root directory of the project
        """
        self.project_root = project_root
        self.docs_dir = os.path.join(project_root, 'docs')
        
        # Ensure docs directory exists
        os.makedirs(self.docs_dir, exist_ok=True)

    def generate_api_documentation(self):
        """
        Generate comprehensive API documentation
        Uses pdoc for Python module documentation
        """
        # Configure pdoc
        pdoc.render.env.loader.searchpath.append(self.project_root)
        
        # Modules to document
        modules = [
            'email_organizer_app',
            'security_engine',
            'email_processor',
            'ml_classifier',
            'database',
            'api'
        ]
        
        for module in modules:
            try:
                output = pdoc.render.html(
                    module, 
                    docformat='google', 
                    include_undocumented=False
                )
                
                with open(os.path.join(self.docs_dir, f'{module}_docs.html'), 'w') as f:
                    f.write(output)
            except Exception as e:
                print(f"Error generating docs for {module}: {e}")

    def generate_markdown_docs(self):
        """
        Generate markdown documentation from project files
        """
        markdown_files = [
            'README.md',
            'CONTRIBUTING.md',
            'ARCHITECTURE.md',
            'SECURITY.md'
        ]
        
        for md_file in markdown_files:
            full_path = os.path.join(self.project_root, md_file)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    content = f.read()
                
                # Convert to HTML
                html_content = markdown2.markdown(content)
                
                # Save HTML version
                with open(os.path.join(self.docs_dir, f'{md_file.replace(".md", ".html")}'), 'w') as f:
                    f.write(html_content)

    def generate_config_documentation(self):
        """
        Generate documentation for configuration files
        """
        config_files = [
            'email_organizer_config.json',
            'email_organizer_security_config.json'
        ]
        
        for config_file in config_files:
            full_path = os.path.join(self.project_root, config_file)
            
            with open(full_path, 'r') as f:
                config = json.load(f)
            
            # Convert to markdown
            markdown_content = "# Configuration Documentation\n\n"
            markdown_content += self._generate_config_markdown(config)
            
            # Save markdown
            with open(os.path.join(self.docs_dir, f'{config_file.replace(".json", "_docs.md")}'), 'w') as f:
                f.write(markdown_content)

    def _generate_config_markdown(self, config: dict, indent: int = 0) -> str:
        """
        Recursively convert config to markdown
        
        Args:
            config (dict): Configuration dictionary
            indent (int): Current indentation level
        
        Returns:
            str: Markdown representation of config
        """
        markdown = ""
        indent_str = "  " * indent
        
        for key, value in config.items():
            if isinstance(value, dict):
                markdown += f"{indent_str}## {key.replace('_', ' ').title()}\n\n"
                markdown += self._generate_config_markdown(value, indent + 1)
            elif isinstance(value, list):
                markdown += f"{indent_str}### {key.replace('_', ' ').title()}\n\n"
                for item in value:
                    markdown += f"{indent_str}- {item}\n"
                markdown += "\n"
            else:
                markdown += f"{indent_str}- **{key.replace('_', ' ').title()}**: {value}\n"
        
        return markdown

    def generate_swagger_docs(self):
        """
        Generate Swagger/OpenAPI documentation
        """
        try:
            # Assumes FastAPI is used and generates Swagger docs
            subprocess.run([
                'python', '-m', 'uvicorn', 
                'api:app', 
                '--generate-swagger-docs', 
                '--output-file', os.path.join(self.docs_dir, 'swagger.json')
            ], check=True)
        except Exception as e:
            print(f"Error generating Swagger docs: {e}")

    def build_documentation_site(self):
        """
        Build comprehensive documentation site
        """
        # Copy static assets
        shutil.copytree(
            os.path.join(self.project_root, 'docs_assets'), 
            os.path.join(self.docs_dir, 'assets'),
            dirs_exist_ok=True
        )
        
        # Generate index.html
        index_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Revvel Email Organizer Documentation</title>
            <link rel="stylesheet" href="assets/styles.css">
        </head>
        <body>
            <nav>
                <a href="api_docs.html">API Documentation</a>
                <a href="README.html">Read Me</a>
                <a href="SECURITY.html">Security</a>
            </nav>
            <main>
                <h1>Revvel Email Organizer Documentation</h1>
                <!-- Add more content as needed -->
            </main>
        </body>
        </html>
        """
        
        with open(os.path.join(self.docs_dir, 'index.html'), 'w') as f:
            f.write(index_html)

def main():
    # Project root directory
    project_root = "/home/openclaw/.openclaw/workspace"
    
    # Initialize documentation generator
    doc_generator = DocumentationGenerator(project_root)
    
    # Generate documentation
    doc_generator.generate_api_documentation()
    doc_generator.generate_markdown_docs()
    doc_generator.generate_config_documentation()
    doc_generator.generate_swagger_docs()
    doc_generator.build_documentation_site()

    print("Documentation generation complete!")

if __name__ == "__main__":
    main()