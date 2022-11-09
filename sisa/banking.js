// ----------------------------------------------------------------------------------------------->>>LOGIN

function login(){
    let username=document.getElementById("username").value;
    let password=document.getElementById("password").value;
    console.log(username,password);

var myHeaders = new Headers();
myHeaders.append("Authorization", "Basic " + btoa(username + ":" + password)); 

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  redirect: 'follow',             // Kalau tidak dikasih maka defaultnya = follow. Follow akan me-redirect ke url, manual tidak.
  credential: 'include'
};

fetch("http://127.0.0.1:5000/login", requestOptions)
  .then((response) => response.json())
  // .then(data => beranda(data))
  .then((result) => {
    console.log(result.token), setcookies("token", result.token, 1);
    localStorage.setItem("usrid", result.usrid);
    window.location.assign("http://127.0.0.1:5500/beranda.html")
   
    // document.cookie = "token="+JSON.parse(result)+"; expires=Thu, 18 Dec 2023 12:00:00 UTC; path=/";
})
.catch(error => console.log('error', error));

};

function setcookies(cName, cValue, expDays) {
  let date = new Date();
  date.setTime(date.getTime() + expDays * 24 * 60 * 60 * 1000);
  const expires = "expires=" + date.toUTCString();
  document.cookie = cName + "=" + cValue + ";" + expires + ";path=/";
}

//tombol login
function klikLogin(){
  location.href = "login.html"
}

// ----------------------------------------------------------------------------------------------->>>BERANDA
function beranda(data){
  if (data === "false"){
    alert("username atau password anda salah!")
  } else{
    alert("Selamat datang di Bank Alltale");
    location.href = "beranda.html";
  }
}

// ----------------------------------------------------------------------------------------------->>>Buat Akun
function buatAkun(){
  location.href = "register.html"
}

// ----------------------------------------------------------------------------------------------->>>LOGOUT
function logout() {
  document.cookie = "token=; expires=Thu, 01 jan 1970 00:00:00 UTC; path=/;";
  window.location.assign("http://127.0.0.1:5500/login.html?#")
}

// ----------------------------------------------------------------------------------------------->>>Transfer
function transfer() {
  // document.cookie = "token=; expires=Thu, 01 jan 1970 00:00:00 UTC; path=/;";
  window.location.assign("http://127.0.0.1:5500/transfer.html")
}

function klikBeranda(){
  location.href = "beranda.html"
}

function klikHistory(){
  location.href = "history.html"
}

function klikPengaturan(){
  location.href = "pengaturan.html"
}

function klikEdit(){
  location.href = "edit.html"
}

function klikKembali(){
  location.href = "pengaturan.html"
}

//Untuk mencegah masuk ke Beranda tanpa Login
// function loginDulu(){
//   let kukis = document.cookie
//   console.log(kukis)
//   let x = kukis.split("=")
//   let y = x[1]

//   if (y == null){
//     window.location.href="login.html"
//     console.log("tes")
//   }
// }

// loginDulu()


//----------------------------------------------------------------------------------------------->>>REGISTER

function register(){
  let nik=document.getElementById("nik").value;
  let nama=document.getElementById("nama").value;
  let no_hp=document.getElementById("no_hp").value;
  let pekerjaan=document.getElementById("pekerjaan").value;
  // let alamat=document.getElementById("alamat").value;
  // let kota=document.getElementById("kota").value;
  // let kelurahaan=document.getElementById("kelurahaan").value;
  // let kecamatan=document.getElementById("kecamatan").value;
  // let provinsi=document.getElementById("provinsi").value;
  // let kodePos=document.getElementById("kodePos").value;
  let username=document.getElementById("username").value;
  let email=document.getElementById("email").value;
  let password=document.getElementById("password").value;
  let saldo=document.getElementById("saldo").value;
  let jenis=document.getElementById("jenis").value;
  let id_cabang=document.getElementById("id_cabang").value;
  console.log(username,password);

var myHeaders = new Headers();
myHeaders.append("Authorization", "Basic cmFmaTIxOjEyMw==");
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "nik": nik,
  "nama": nama,
  "no_hp": no_hp,
  "pekerjaan": pekerjaan,
  "username": username,
  "email": email,
  "password": password,
  "saldo": saldo,
  "jenis": jenis,
  "id_cabang": id_cabang
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

if (nik =="" || nama =="" || no_hp =="" || pekerjaan =="" || username =="" || email == "" || password == ""){           // A field can not be empty
  return alert("Setiap kolom harus di isi")
} else if (password.length < 8){                                    // Password length at least 8 characters
  return alert("Password minimal panjang 8 karakter")
} else if (/[0-9]/.test(password) === false){                       // Password must contain at least a number
 return alert("Password harus terdapat berupa angka")
} else if (/[a-zA-Z]/.test(password) === false){                    // Password must contain at least a letter
 return alert("Password harus terdapat berupa huruf")
// } else if (password !== passRepeat){                                // Password shoud match
//  return alert("Those passwords didn't match. Try again.")
} else if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) === false){          // Email address validation
 return alert("Tolong masukan email anda yang tervalidasi")
// } else if (phone.length <= 8 || /^\+(?:[0-9] ?){6,14}[0-9]$/.test(phone)=== false){                          // Phone number validation
//  return alert("masukan nomor telepon anda menggunakan format (+62)")
} else {   
  fetch("http://127.0.0.1:5000/nasabah/register", requestOptions)
    .then(response => response.text())
    .then(data => {return (data !== "False")? alert("Berhasil membuat akun."):
  alert("gagal membuat akun karena username anda sudah ada yang pakai. Silahkan coba lagi dengan username yang lain")})
    .catch(error => alert("email atau nomor handphone anda telah dipakai di akun lain." + error));
  }
}


//----------------------------------------------------------------------------------------------->>>Nampilin Username di dpn
function checkCookie() {
  const token = document.cookie;
  // console.log(token);
  if (token !== "") {
      // document.getElementById('loginbutton').style.display = "none"; untuk web yang bisa lihat tanpa login
      const split = token.split(".");
      let parsedToken = JSON.parse(atob(split[1]));
      // console.log(parsedToken)
      let namaNasabah = parsedToken["nama"]  
      let username = parsedToken["usrname"]
      // console.log(nama)
      let userLabel = document.getElementById('userprofile')
      let userLabe = document.getElementById('usernm');
      userLabel.innerHTML = namaNasabah;
      userLabe.innerHTML = username;
  } else {
      document.getElementById('userprofile').style.display = "none";
      document.getElementById('usernm').style.display = "none";
  }
}

// function checkCookie() {
//   const token = document.cookie;
//   // console.log(token);
//   if (token !== "") {
//       // document.getElementById('loginbutton').style.display = "none"; untuk web yang bisa lihat tanpa login
//       const split = token.split(".");
//       let parsedToken = JSON.parse(atob(split[1]));
//       let username = parsedToken["usrname"]
//       let userLabel = document.getElementById('userpnm');
//       userLabel.innerHTML = nama
//       userLabel.innerHTML = username;
//   } else {
//       document.getElementById('userprofile').style.display = "none";
//   }
// }


//----------------------------------------------------------------------------------------------->>>Nampilin profile
function loadprofile(){
  let idusr= localStorage.getItem("usrid")  
 
  var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:5000/account/profile/"+idusr, requestOptions)
  .then(response => response.json())
  .then((result) =>{ 
       var arr = []
       arr = result
        //  console.log(arr) 
         profilAkun = document.getElementById("profil")
         for (i = 0; i < arr.length; i++) { 
          // console.log(arr[i].saldo)
           profilAkun.innerHTML += 
           `
            <ul>
           <div class="konten-info">
             <p class="logo baru">></p>
             <div class="hist">
               <p class="h-name" >Rp ${arr[i].saldo}</p>
               <p class="h-date">${arr[i].status}</p>
             </div>
             <hr>
             <p>${arr[i].no_rekening}</p>
           </div>
           </ul>`
        }
       })  

  
  .catch(error => console.log('error', error));

}




//----------------------------------------------------------------------------------------------->>>Nampilin History

function loadHistory(){
  let idusr= localStorage.getItem("usrid") 
  var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:5000/transaksi/history/"+idusr , requestOptions)
    .then(response => response.json())
    .then((result) =>{ 
          var arr = []
          arr = result
          // console.log(arr)
          historyAkun = document.getElementById("history")
          for (i = 0; i < arr.length; i++) { 
            // console.log(arr[i].id_pengirim) 
            if (arr[i].id_penerima !== arr[i].id_pengirim ){
            historyAkun.innerHTML +=
             `<ul>
              <div class="konten-info">
                <p class="logo baru">-</p>
                  <div class="hist">
                    <p class="h-name">${arr[i].id_penerima}</p>
                    <p class="h-date">${arr[i].waktu}</p>
                  </div>
                    <p class="h-rate-down">${arr[i].saldo_keluar}</p>
              </div>
              </ul>
             ` 
            }else{
            historyAkun.innerHTML +=
             `<ul>
              <div class="konten-info">
                <p class="logo baru">+</p>
                  <div class="hist">
                    <p class="h-name">${arr[i].id_pengirim}</p>
                    <p class="h-date">${arr[i].waktu}</p>
                  </div>
                    <p class="h-rate-up">${arr[i].saldo_masuk}</p>
              </div>
              </ul>
             ` 
            }
          }
          })
    .catch(error => console.log('error', error));
}

//----------------------------------------------------------------------------------------------->>>Nampilin Profil
function loadNasabah(){
let idusr= localStorage.getItem("usrid") 

var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};

fetch("http://127.0.0.1:5000/nasabah/profile/"+idusr, requestOptions)
  .then(response => response.json())
  .then((result) =>{ 
    var arr = []
    arr = result
    console.log(arr)
    dataAkun = document.getElementById("dataDiri")
    for (i=0; i< arr.length; i++){
      // console.log(arr[i].nama)
      dataAkun.innerHTML +=
      `
      <div class="input-field">
        <label class="label" for="first">Nama</label>
        <p>${arr[i].nama} </p>
      </div>
      <div class="input-field">
        <label class="label" for="last">No. Handphone</label>
        <p>${arr[i].no_hp} </p>
      </div>
      <div class="input-field">
        <label class="label" for="email">Email</label>
        <p>${arr[i].email} </p>
      </div>
      <div class="input-field">
        <label class="label" for="pekerjaan">Pekerjaan</label>
        <p> ${arr[i].pekerjaan}</p>
      </div>
      <div >
        <button onclick="klikEdit()" class="upload-pp-btn f">Edit</button>
      </div>
      `
    }
  }
  )
  .catch(error => console.log('error', error));
}

//----------------------------------------------------------------------------------------------->>>Edit/Update
// cara pake cookies (belum jalan)
function updateAkun(){
  let idusr= localStorage.getItem("usrid")
  
  let nama = document.getElementById('nama').value;
  let no_hp = document.getElementById('noHP').value;
  let pekerjaan = document.getElementById('pekerjaan').value;
  let email = document.getElementById('email').value;

  
  var raw = json.stringify({
    "nama": nama,
    "no_hp": no_hp,
    "pekerjaan": pekerjaan,
    "email": email,
  });

  // const changeForm = document.querySelector("#changeForm");
  //       let changeData = new FormData(changeForm);
  //       changeData = Object.fromEntries(changeData);

        // for(let key in changeData){
        //     let value = changeData[key];
        //     if(value == ""){
        //         delete preRaw[key];   
        //     }
        // }

  
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  // myHeaders.append("Authorization","Basic " + btoa(username + ":" + password));
  
  var requestOptions = {
    method: 'PUT',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };
  
  fetch("http://127.0.0.1:5000/nasabah/update/"+ idusr, requestOptions)
    .then(response => response.json())
    .then(result => {
      console.log(result)
      alert("Data anda telah diperbaharui")
      window.location.href="pengaturan.html"
    })
    .catch(error => {
      console.log('error', error)
      alert("gagal mempebaharui profil")});
// }
}

//cara pake localStorage

// function updateAkun(){
//   let idusr= localStorage.getItem("usrid")
//   var requestOptions = {
//     method: 'PUT',
//     redirect: 'follow'
//   };
  
//   fetch("http://127.0.0.1:5000/nasabah/update/"+idusr, requestOptions)
//     .then(response => response.text())
//     .then(result => 
      
//       )
//     .catch(error => console.log('error', error));
// }