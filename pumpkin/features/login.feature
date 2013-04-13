# language: id
Fitur: Login
  Dalam rangka untuk melakukan validasi user
  Sebagai user
  Saya ingin login ke dalam sistem

  Skenario: User login
    Dengan memiliki username "ted" dan password "t3d"
    Ketika saya membuka halaman dengan session baru
    Maka saya akan diarahkan ke halaman login
    Ketika mengisikan username "ted"
    Dan mengisikan password "t3d"
    Dan melakukan submit form
    Maka Saya akan menuju pada halaman utama

