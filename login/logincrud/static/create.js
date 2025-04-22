// create user 
document.getElementById("userFormCreate").addEventListener("submit", async function (event) {
    event.preventDefault();  // Prevent default form submission

    const form = event.target;
    const formData = new FormData(form);
    const data = {};

    // Convert FormData to a plain object
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        // Send the data to the server using fetch
        const response = await fetch('/create/user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Authorization':`Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(data) // Send data as JSON
        });
        console.log('X-CSRFToken    ',document.querySelector('[name=csrfmiddlewaretoken]').value)
        console.log("authorization token  :  ",localStorage.getItem('access_token'))
        // Get the response in JSON format
        const result = await response.json();

        if (response.ok) {
            // If the user was created successfully
            document.querySelector('.messageBody').innerHTML = `${result.message}`;
            document.querySelector('.alertMessage').style.display = 'block';
            setTimeout(() => {
                document.querySelector('.alertMessage').style.display = 'none';
            }, 2000);
            setTimeout(()=>{
                window.location.href = "/dashboard";  // Redirect to the user list page (change the URL based on your requirements)
            },1000)
            // alert(result.message);  // Show success message
        } else {
            // Handle form validation errors or other server-side issues
            if (result.errors) {
                let errorMessages = "";
                for (let field in result.errors) {
                    errorMessages += `${field}: ${result.errors[field].join(', ')}\n`;
                }
                document.querySelector('.messageHeader').innerHTML = 'Error!';
            document.querySelector('.messageBody').innerHTML = `${errorMessages}`;
            document.querySelector('.alertMessage').style = 'display:block;background-color: #d3b0b0;';
                // alert("Form errors:\n" + errorMessages);  // Display validation errors
            } else if (result.error) {
                alert("Error: " + result.error);  // Display general error
            }
        }
    } catch (error) {
        // Handle network or other unexpected errors
        alert("There was an error processing your request: " + error.message);
    }
});

fetch('/dashboard/', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')  // or a cookie
    }
})
.then(response => response.json())
.then(data => console.log(data));

// update user

async function updateUser(pk, data) {
    function generateCSRFToken() {
        return btoa(String(Math.random() + Date.now())); // Basic random token
    }
    console.log(data.mobile_number)
    // document.querySelector('#update-btn').innerHTML = 'Update';
    const csrfToken = generateCSRFToken();
    console.log(csrfToken, "csrfffffffffffffffff")
    try {
        console.log("update function triggered")
        const response = await fetch(`http://127.0.0.1:8000/users/update/${pk}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization':`Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(data)
        });
        
        const responsedata = await response.json();
        
        if (response.ok) {
            alert("user updated successfully");
            setTimeout(() => {
                window.location.href = 'http://127.0.0.1:8000/dashboard/';
            }, 2000); // 2 seconds
        } else {
            console.error(responsedata.errors || responsedata.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}
//   document.getElementById('UpdateForm').addEventListener('submit',function(){
    //     updateUser();
    //   })
    // Example delete user
    function deleteUser(pk){
        console.log("delete function")
        axios.delete(`/users/delete/${pk}/`)
        console.log(pk)
        alert("User Deleted")
        window.location.reload();
        // .then(response => {
            //     console.log(response.status); // 200
            //     alert('User deleted!');
            //     window.location.reload();
            // })
            // .catch(error => {
                //     console.error(error);
                //     alert('Error deleting user');
                // });
            }
            
            // pop up operations for delete 
            
            function popupdelete(pk){
                console.log("okk",pk)
                document.querySelector('.pop-up-delete').style.display = 'block';
                // document.querySelector('.pop-up-delete').style.display = 'none';
                document.querySelector('.delete-actions').addEventListener('click',()=>{
                    console.log("del",pk)
                    deleteUser(pk)
                })
            }
            function cancel(){
                console.log("logout onclick");
                document.querySelector('.pop-up-delete').style.display = 'none';
            }            

            // document.querySelector('.delete-actions').addEventListener('click',()=>{
                //     console.log("del")
                // })
                
                
                
                // function updateUser(pk,data){
                    // axios.put(`/api/update/${pk}/`, data)
                    // .then(response => {
//   console.log(response.status); // 200
//   alert('User updated!');
// })
// .catch(error => {
    //   console.error(error.response.data);
    //   alert('Error: ' + JSON.stringify(error.response.data));
    // });
  
    
    // async function UserData(e) {
    //     const userData = {
    //         user_name: document.getElementById('user_name').value,
    //         user_role: document.getElementById('user_role').value,
    //         email_id: document.getElementById('email_id').value,
    //         department: document.getElementById('department').value,
    //         employee_id: document.getElementById('employee_id').value,
    //         designation: document.getElementById('designation').value,
    //         mobile_number: document.getElementById('mobile_number').value,
    //         is_active: document.querySelector('input[name="is_active"]:checked').value === "True",
    //         is_locked: document.querySelector('input[name="is_locked"]:checked').value === "True",
    //         remarks1: document.getElementById('remarks1').value,
    //         remarks2: document.getElementById('remarks2').value
    //     };
    //     function generateCSRFToken() {
    //         return btoa(String(Math.random() + Date.now())); // Basic random token
    //     }
    //     const csrfToken = generateCSRFToken();
    //     console.log(csrfToken, "csrfffffffffffffffff")
    //     try {
    //         const response = await fetch('http://127.0.0.1:8000/create/user/', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'X-CSRFToken': csrfToken,
                    
    //             },
    //             body: JSON.stringify(userData)
    //         });
    
    //         const data = await response.json();
    
    //         if (response.ok) {
    //             alert(data.message);
    //             window.location.href = 'http://127.0.0.1:8000/dashboard/';
    //             // setTimeout(() => {
    //             //     window.location.href = 'http://127.0.0.1:8000/dashboard/';
    //             // }, 2000); // 2 seconds
    //         } else {
    //             e.preventDefault();
    //             console.error(data.errors || data.error);
    //         }
    //     } catch (error) {
    //         console.error('Network error:', error);
    //     }
    // }
// }