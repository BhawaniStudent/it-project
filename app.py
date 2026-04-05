const express = require("express");
const app = express();
const PORT = 3000;

app.use(express.json());

// Data
let assets = [
  { id: 1, name: "Computer", category: "Hardware", status: "Available", date: new Date().toLocaleDateString() },
  { id: 2, name: "Server", category: "Hardware", status: "In Use", date: new Date().toLocaleDateString() }
];

// LOGIN PAGE
app.get("/", (req, res) => {
  res.send(`
  <html>
  <head>
    <title>Login</title>
    <style>
      body {
        font-family: Arial;
        background: linear-gradient(135deg,#667eea,#764ba2);
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
      }
      .box {
        background:white;
        padding:30px;
        border-radius:10px;
        text-align:center;
        box-shadow:0 5px 15px rgba(0,0,0,0.3);
      }
      input {
        width:200px;
        padding:10px;
        margin:10px;
      }
      button {
        padding:10px 20px;
        background:#667eea;
        color:white;
        border:none;
        cursor:pointer;
      }
    </style>
  </head>
  <body>
    <div class="box">
      <h2>IT Asset Login</h2>
      <input id="user" placeholder="Username"><br>
      <input id="pass" type="password" placeholder="Password"><br>
      <button onclick="login()">Login</button>
    </div>

    <script>
      function login(){
        if(user.value==="admin" && pass.value==="1234"){
          window.location="/dashboard";
        } else {
          alert("Invalid Login");
        }
      }
    </script>
  </body>
  </html>
  `);
});

// DASHBOARD
app.get("/dashboard", (req, res) => {
  res.send(`
  <html>
  <head>
    <title>Dashboard</title>
    <style>
      body { font-family:Arial; margin:0; background:#f5f6fa; }
      header {
        background:#2f3640;
        color:white;
        padding:15px;
        text-align:center;
      }
      .container { padding:20px; }

      input, select {
        padding:8px;
        margin:5px;
      }

      button {
        padding:8px 12px;
        margin:5px;
        border:none;
        background:#273c75;
        color:white;
        cursor:pointer;
      }

      table {
        width:100%;
        border-collapse:collapse;
        margin-top:20px;
        background:white;
      }

      th, td {
        border:1px solid #ddd;
        padding:10px;
        text-align:center;
      }

      th {
        background:#273c75;
        color:white;
      }
    </style>
  </head>

  <body>
    <header>
      <h1>IT Asset Management System</h1>
    </header>

    <div class="container">

      <h3>Add / Update Asset</h3>
      <input id="id" placeholder="ID">
      <input id="name" placeholder="Name">
      <input id="category" placeholder="Category">

      <select id="status">
        <option>Available</option>
        <option>In Use</option>
      </select>

      <button onclick="add()">Add</button>
      <button onclick="update()">Update</button>

      <h3>Search</h3>
      <input id="search" onkeyup="search()" placeholder="Search assets">

      <table>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Category</th><th>Status</th><th>Date</th><th>Actions</th>
          </tr>
        </thead>
        <tbody id="table"></tbody>
      </table>

    </div>

    <script>
      let data = [];

      async function load(){
        const res = await fetch('/api/assets');
        data = await res.json();
        show(data);
      }

      function show(arr){
        table.innerHTML="";
        arr.forEach(a=>{
          table.innerHTML += \`
            <tr>
              <td>\${a.id}</td>
              <td>\${a.name}</td>
              <td>\${a.category}</td>
              <td>\${a.status}</td>
              <td>\${a.date}</td>
              <td>
                <button onclick="fill(\${a.id})">Edit</button>
                <button onclick="del(\${a.id})">Delete</button>
              </td>
            </tr>
          \`;
        });
      }

      function search(){
        const val = search.value.toLowerCase();
        show(data.filter(a=>a.name.toLowerCase().includes(val)));
      }

      function fill(idVal){
        const a = data.find(x=>x.id==idVal);
        id.value = a.id;
        name.value = a.name;
        category.value = a.category;
        status.value = a.status;
      }

      async function add(){
        await fetch('/api/assets',{
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({
            name:name.value,
            category:category.value,
            status:status.value
          })
        });
        load();
      }

      async function update(){
        await fetch('/api/assets/'+id.value,{
          method:'PUT',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({
            name:name.value,
            category:category.value,
            status:status.value
          })
        });
        load();
      }

      async function del(idVal){
        await fetch('/api/assets/'+idVal,{method:'DELETE'});
        load();
      }

      load();
    </script>

  </body>
  </html>
  `);
});

// API
app.get("/api/assets",(req,res)=> res.json(assets));

app.post("/api/assets",(req,res)=>{
  const newAsset = {
    id: assets.length+1,
    name:req.body.name,
    category:req.body.category,
    status:req.body.status,
    date:new Date().toLocaleDateString()
  };
  assets.push(newAsset);
  res.json(newAsset);
});A

app.put("/api/assets/:id",(req,res)=>{
  const a = assets.find(x=>x.id==req.params.id);
  if(a){
    a.name=req.body.name;
    a.category=req.body.category;
    a.status=req.body.status;
  }
  res.json(a);
});

app.delete("/api/assets/:id",(req,res)=>{
  assets = assets.filter(x=>x.id!=req.params.id);
  res.json({msg:"Deleted"});
});

app.listen(PORT,()=>{
  console.log("Server running at http://localhost:3000");
});
