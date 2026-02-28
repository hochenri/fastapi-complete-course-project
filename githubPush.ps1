param (
    [string]$Desc = "Project update"
)
git remote add origin https://github.com/hochenri/fastapi-complete-course-project.git
git add .
git commit -m $Desc
git push -u origin main