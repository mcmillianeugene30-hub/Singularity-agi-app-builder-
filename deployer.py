import requests
import os
import subprocess

class Deployer:
    """
    Singularity AGI Deployer Module
    Automates GitHub repo creation and Netlify deployment.
    """
    
    def __init__(self, github_token: str, netlify_token: str):
        self.github_token = github_token
        self.netlify_token = netlify_token

    def deploy_to_netlify(self, project_path: str, repo_name: str):
        """
        Full-stack deployment pipeline:
        1. Create GitHub Repo
        2. Push generated code
        3. Link to Netlify (via Netlify API)
        """
        print(f"[*] Deploying project: {repo_name}")
        
        # 1. Create GitHub Repository
        try:
            url = "https://api.github.com/user/repos"
            headers = {"Authorization": f"token {self.github_token}"}
            payload = {"name": repo_name, "private": False}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            repo_url = response.json()['clone_url']
            print(f"[+] Created GitHub repo: {repo_url}")
        except Exception as e:
            print(f"[!] GitHub repo creation failed: {e}")
            return

        # 2. Git Push (requires git installed locally)
        try:
            os.chdir(project_path)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from Singularity AGI"], check=True)
            
            # Authenticated URL for pushing
            auth_repo_url = repo_url.replace("https://", f"https://{self.github_token}@")
            subprocess.run(["git", "remote", "add", "origin", auth_repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print(f"[+] Pushed code to GitHub.")
        except Exception as e:
            print(f"[!] Git push failed: {e}")
            return

        # 3. Create Netlify Site (Simple Example)
        # Note: Linking GitHub to Netlify via API is complex; often done via CLI or manual UI.
        # This example creates a simple site.
        try:
            url = "https://api.netlify.com/api/v1/sites"
            headers = {"Authorization": f"Bearer {self.netlify_token}"}
            payload = {"name": repo_name}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"[+] Created Netlify site: {response.json()['url']}")
        except Exception as e:
            print(f"[!] Netlify site creation failed: {e}")

# Example:
# deployer = Deployer(os.getenv("GITHUB_TOKEN"), os.getenv("NETLIFY_TOKEN"))
# deployer.deploy_to_netlify("/workspace/generated_app", "my-ai-fitness-app")
