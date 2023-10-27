import os

from dotenv import load_dotenv

from config import Config

class GitProject:
	def __init__(self, project_directory):
		self.project_directory = project_directory

	def add(self):
		os.chdir(self.project_directory)
		os.system("git add .")

	def status(self):
		os.system("git status")

	def commit(self, commit_description):
		os.system(f'git commit -m "{commit_description}"')

	def push(self):
		os.system("git push -u origin main")

	def print_completed(self):
		self.status()
		print("Project successfully pushed to the remote repository.")


def main():
	load_dotenv()

	name_github = os.getenv("GITHUB_USERNAME")
	token_github = os.getenv("GITHUB_TOKEN")

	if name_github is None or token_github is None:
		print("GitHub credentials not found in the .env file.")
		return

	os.environ['GITHUB_USERNAME'] = os.getenv("GITHUB_USERNAME")
	os.environ['GITHUB_TOKEN'] = os.getenv("GITHUB_TOKEN")
	
	config = Config()
	current_path = config.current_path

	# Create a GitProject instance
	my_project = GitProject(current_path)

	my_project.add()
	my_project.status()

	commit_description = input("Enter commit description: ")

	my_project.commit(commit_description)
	my_project.push()

	my_project.print_completed()


if __name__ == "__main__":
	main()
