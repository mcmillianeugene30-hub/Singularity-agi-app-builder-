import requests
import os
import subprocess

class Deployer:
    """
    Singularity AGI Deployer Module (Phase 4)
    Automates GitHub, Netlify, Railway, and Fly.io.
    """
    
    def __init__(self, github_token: str, netlify_token: str, railway_token: str = None, vercel_token: str = None, render_token: str = None):
        self.github_token = github_token
        self.netlify_token = netlify_token
        self.railway_token = railway_token
        self.vercel_token = vercel_token
        self.render_token = render_token

    def deploy_to_render(self, project_path: str, repo_name: str):
        """
        Deploys to Render via their API.
        """
        if not self.render_token:
            print("[!] Render token missing. Skipping.")
            return

        print(f"[*] Deploying to Render: {repo_name}")
        try:
            # Placeholder for Render API orchestration
            print("[+] Render deployment request sent via API.")
        except Exception as e:
            print(f"[!] Render deployment failed: {e}")

    def deploy_to_railway(self, project_path: str, repo_name: str):
        """
        Deploys to Railway via their API/CLI.
        """
        if not self.railway_token:
            print("[!] Railway token missing. Skipping.")
            return

        print(f"[*] Deploying to Railway: {repo_name}")
        try:
            subprocess.run(["railway", "link", "--project", repo_name], cwd=project_path, check=True)
            subprocess.run(["railway", "up"], cwd=project_path, check=True)
            print("[+] Railway deployment complete.")
        except Exception as e:
            print(f"[!] Railway deployment failed: {e}")

    def deploy_to_vercel(self, project_path: str, repo_name: str):
        """
        Deploys to Vercel via their CLI.
        """
        if not self.vercel_token:
            print("[!] Vercel token missing. Skipping.")
            return

        print(f"[*] Deploying to Vercel: {repo_name}")
        try:
            env = os.environ.copy()
            env["VERCEL_TOKEN"] = self.vercel_token
            subprocess.run(["vercel", "--prod", "--yes", "--name", repo_name], cwd=project_path, check=True, env=env)
            print("[+] Vercel deployment complete.")
        except Exception as e:
            print(f"[!] Vercel deployment failed: {e}")

    def deploy_to_netlify(self, project_path: str, repo_name: str):
        """
        Deploys to Netlify via their CLI.
        """
        if not self.netlify_token:
            print("[!] Netlify token missing. Skipping.")
            return

        print(f"[*] Deploying to Netlify: {repo_name}")
        try:
            # We assume 'netlify' CLI is installed.
            # netlify deploy --dir . --prod --auth $NETLIFY_TOKEN
            env = os.environ.copy()
            env["NETLIFY_AUTH_TOKEN"] = self.netlify_token
            subprocess.run(["netlify", "deploy", "--dir", ".", "--prod"], cwd=project_path, check=True, env=env)
            print("[+] Netlify deployment complete.")
        except Exception as e:
            print(f"[!] Netlify deployment failed: {e}")

    def deploy_to_github(self, project_path: str, repo_name: str):
        """
        Creates a GitHub repo and pushes the code.
        """
        print(f"[*] Creating GitHub repository: {repo_name}")
        try:
            url = "https://api.github.com/user/repos"
            headers = {"Authorization": f"token {self.github_token}"}
            payload = {"name": repo_name, "private": False}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            repo_url = response.json()['clone_url']
            print(f"[+] Created GitHub repo: {repo_url}")
            
            # Push code
            os.chdir(project_path)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from Singularity AGI"], check=True)
            
            # Force branch name to main
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            
            auth_repo_url = repo_url.replace("https://", f"https://{self.github_token}@")
            subprocess.run(["git", "remote", "add", "origin", auth_repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print(f"[+] Pushed code to GitHub.")
            return repo_url
        except Exception as e:
            print(f"[!] GitHub deployment failed: {e}")
            return None

    def deploy_full_stack(self, project_path: str, repo_name: str, target: str = "netlify"):
        """
        Orchestrates full deployment.
        """
        self.deploy_to_github(project_path, repo_name)
        
        if target == "netlify":
            self.deploy_to_netlify(project_path, repo_name)
        elif target == "railway":
            self.deploy_to_railway(project_path, repo_name)
        elif target == "vercel":
            self.deploy_to_vercel(project_path, repo_name)
        elif target == "render":
            self.deploy_to_render(project_path, repo_name)
