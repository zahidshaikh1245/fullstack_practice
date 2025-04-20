let token = "";

async function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://localhost:5000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  if (res.status === 201) {
    token = data.token;
    showResponse("Registered! Token saved.");
  } else {
    showResponse(data.msg);
  }
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  if (res.ok) {
    token = data.token;
    showResponse("Logged in! Token saved.");
  } else {
    showResponse(data.msg);
  }
}

async function getProtected() {
  if (!token) {
    return showResponse("No token found. Please log in.");
  }

  const res = await fetch("http://localhost:5000/protected", {
    method: "GET",
    headers: {
      Authorization: token
    }
  });

  const data = await res.json();
  showResponse(data.msg || "Unknown error");
}

function showResponse(message) {
  document.getElementById("response").innerText = message;
}
