document.addEventListener("DOMContentLoaded", function () {
    // Fetch token from localStorage for later use
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('You must be logged in to access the dashboard.');
        window.location.href = 'login.php';
        return;
    }

    // Handle logout
    document.getElementById('logout').addEventListener('click', function () {
        localStorage.removeItem('access_token');
        window.location.href = 'login.php';
    });

    // Fetch projects after successful login
    fetch('http://127.0.0.1:8000/projects', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response.json())
        .then(projects => {
            let projectList = document.getElementById('projectList');
            projects.forEach(project => {
                let projectCard = createProjectCard(project);
                projectList.innerHTML += projectCard;
            });

            // Add event listeners for editing and deleting
            document.querySelectorAll('.editProject').forEach(button => {
                button.addEventListener('click', function () {
                    const projectId = this.getAttribute('data-id');
                    editProject(projectId);
                });
            });

            document.querySelectorAll('.deleteProject').forEach(button => {
                button.addEventListener('click', function () {
                    const projectId = this.getAttribute('data-id');
                    deleteProject(projectId);
                });
            });
        })
        .catch(error => console.error('Error fetching projects:', error));

    // Function to create a project card
    function createProjectCard(project) {
        const imageSrc = project.images.length > 0 ? `/${project.images[0]}` : '/assets/images/placeholder.jpg';
        const linkButton = project.link
            ? `<a href="${project.link}" target="_blank" class="btn btn-outline-primary">View More</a>`
            : '';

        return `
            <div class="card mb-4" id="project-${project.id}">
                <img src="${imageSrc}" class="card-img-top" alt="${project.title}">
                <div class="card-body">
                    <h5 class="card-title">${project.title}</h5>
                    <p class="card-text">${project.description}</p>
                    ${linkButton}
                    <button class="btn btn-warning editProject" data-id="${project.id}">Edit</button>
                    <button class="btn btn-danger deleteProject" data-id="${project.id}">Delete</button>
                </div>
            </div>
        `;
    }

    // Function to edit project (basic alert, but can be expanded)
    function editProject(projectId) {
        alert('Edit project: ' + projectId);
    }

    // Function to delete project
    function deleteProject(projectId) {
        if (!projectId) {
            console.error('Project ID is missing.');
            alert('Failed to delete project: Project ID is missing.');
            return;
        }

        if (confirm('Are you sure you want to delete this project?')) {
            console.log(`Deleting project with ID: ${projectId}`); // Debugging line

            fetch(`http://127.0.0.1:8000/projects/${projectId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}` // Use token from localStorage
                }
            })
                .then(async response => {
                    if (response.ok) {
                        alert('Project deleted successfully');
                        document.getElementById(`project-${projectId}`).remove(); // Remove the project from the UI
                    } else {
                        const errorDetails = await response.json();
                        console.error('Failed to delete project:', response.status, response.statusText, errorDetails);
                        alert(`Failed to delete project: ${errorDetails.detail || 'Unknown error'}`);
                    }
                })
                .catch(error => {
                    console.error('Error deleting project:', error);
                    alert('An error occurred while deleting the project.');
                });
        }
    }

    // Function to handle "Add New Project" button
    document.getElementById('addProject').addEventListener('click', function () {
        const modal = new bootstrap.Modal(document.getElementById('addProjectModal'));
        modal.show();
    });

    // Handle the form submission for adding a new project
    document.getElementById('addProjectForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const title = document.getElementById('projectTitle').value;
        const description = document.getElementById('projectDescription').value;
        const link = document.getElementById('projectLink').value; // Get the project link
        const imageFiles = document.getElementById('projectImageFile').files;

        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('link', link); // Append the link to the form data

        // Add images to the form data
        for (let i = 0; i < imageFiles.length; i++) {
            formData.append('images', imageFiles[i]);
        }

        fetch('http://127.0.0.1:8000/projects', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        })
            .then(async response => {
                if (!response.ok) {
                    const errorDetails = await response.json();
                    console.error('API Error:', response.status, response.statusText, errorDetails);
                    alert(`Failed to add project: ${errorDetails.detail || 'Unknown error'}`);
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (!data || !data.project_id) {
                    console.error('Invalid API response:', data);
                    alert('Failed to add project: Invalid response from server.');
                    return;
                }

                console.log('Project added:', data);
                alert('Project added successfully');
                const newProject = createProjectCard(data); // Create a new project card from the response
                document.getElementById('projectList').innerHTML += newProject;

                // Close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addProjectModal'));
                modal.hide();
            })
            .catch(error => {
                console.error('Error adding project:', error);
                alert('Failed to add project');
            });
    });
});
