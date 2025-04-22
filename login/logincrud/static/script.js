//login api endpoint
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });

  if (response.ok) {
    console.log("Login status OK", username, password);
    const data = await response.json();
    const jwtToken = data.token;
    console.log(jwtToken, "token")

    // Decode JWT to get email and other info
    const decodedToken = decodeJwt(jwtToken);
    const email = decodedToken.email;

    // Store the JWT token in localStorage
    localStorage.setItem("access_token", jwtToken);

    // Optionally store the user's email or any other details
    localStorage.setItem("user_email", email);

    console.log("Stored JWT token in localStorage", jwtToken);
    window.location.href = "/dashboard";
  } else {
    const result = await response.json();
    console.log("error in fetching jwt Invalid");
    document.querySelector(".login-error").innerHTML =
      "Invalid username or password";
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function decodeJwt(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
}

// Function to get CSRF token from cookies (if needed)
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function logout() {
  // Clear localStorage tokens
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');

  // Optionally clear cookies
  document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

  // Redirect to login page
  window.location.href = '/login/';
}

// //  Get JWT token
// async function getJwtToken(username, password) {
//   try {
//       const res = await fetch("/api/token/", {
//           method: "POST",
//           headers: {
//               "Content-Type": "application/json",
//           },
//           body: JSON.stringify({ username, password }),
//       });
//       if (res.ok) {
//           const data = await res.json();
//           localStorage.setItem("access_token", data.access);
//           localStorage.setItem("refresh_token", data.refresh);
//           console.log("JWT token stored");
//           setTimeout(() => {
//               window.location.href = "/dashboard"; // redirect after token stored
//           }, 5000)

//       } else {
//           console.error("Failed to get JWT token");
//       }
//   } catch (err) {
//       console.error("JWT fetch error:", err);
//   }
// }

// localStorage.setItem("access_token", data.access);
// localStorage.setItem("refresh_token", data.refresh);

// document.getElementById("loginForm").addEventListener("submit", async (e) => {
//   e.preventDefault();

//   const response = await fetch("/", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": getCookie("csrftoken")
//     },
//     body: JSON.stringify({
//       username: document.getElementById("username").value,
//       password: document.getElementById("password").value,
//     }),
//   });
//   const jwt = c
//   if (response.ok) {
//     console.log("login status ok")
//     window.location.href = "/dashboard";
//   } else {
//     const result = await response.json();
//     // alert(result.message || "Login failed");
//     console.log("invalid")
//     document.querySelector('.login-error').innerHTML = "invalid username or password"

//   }
// });
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== "") {
//     const cookies = document.cookie.split(";");
//     for (let cookie of cookies) {
//       cookie = cookie.trim();
//       if (cookie.startsWith(name + "=")) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }



// Function to decode JWT (for extracting the email or any other data)


// display graphs on the dashboard
