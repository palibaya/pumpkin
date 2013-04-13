# language: id
Fitur: Melihat daftar project
  Dalam rangka melihat daftar project yang ada di sistem
  Sebagai user dengan group tertentu
  Saya ingin melihat beberapa project yang terlah dibuat

  Dasar: Memiliki beberapa data awal
    Dengan memiliki beberapa data user:
      | username    | password  | email             | is_admin  |
      | myadmin     | rahasia   | myadmin@mail.com  | 1         |
      | ted         | t3d       | ted@mail.com      | 0         |
      | dick        | d1ck      | dick@mail.com     | 0         |
    Dan memiliki beberapa  data project:
      | name        | identifier    | manager       |
      | Melon       | melon         | ted           |
      | Strawberry  | strawberry    | ted           |
      | Banana      | banana        | dick          |


  Skenario: Melihat semua project menggunakan user admin
    Dengan telah login sebagai "myadmin" menggunakan password "rahasia"
    Ketika mengklik logo sistem
    Maka Saya akan menuju pada halaman utama
    Dan Saya akan melihat daftar project berikut:
      | name        | identifier    |
      | Melon       | melon         |
      | Strawberry  | strawberry    |
      | Banana      | banana        |


  Skenario: Melihat semua project menggunakan user bukan admin
    Dengan telah login sebagai "ted" menggunakan password "t3d"
    Ketika mengklik logo sistem
    Maka Saya akan menuju pada halaman utama
    Dan Saya akan melihat daftar project berikut:
      | name        | identifier    |
      | Melon       | melon         |
      | Strawberry  | strawberry    |




