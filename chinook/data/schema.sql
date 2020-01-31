CREATE TABLE IF NOT EXISTS albums (
  album_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  title nvarchar(160) NOT NULL,
  artist_id integer NOT NULL
);
CREATE TABLE IF NOT EXISTS artists (
  artist_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  name nvarchar(120)
);
CREATE TABLE IF NOT EXISTS customers (
  customer_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  first_name nvarchar(40) NOT NULL,
  last_name nvarchar(20) NOT NULL,
  company nvarchar(80),
  address nvarchar(70),
  city nvarchar(40),
  state nvarchar(40),
  country nvarchar(40),
  postal_code nvarchar(10),
  phone nvarchar(24),
  email nvarchar(60) NOT NULL,
  support_reply_id integer
);
CREATE TABLE IF NOT EXISTS employees (
  employee_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  last_name nvarchar(20) NOT NULL,
  first_name nvarchar(20) NOT NULL,
  title nvarchar(30),
  reports_to integer,
  birthdate datetime,
  hiredate datetime,
  address nvarchar(70),
  city nvarchar(40),
  state nvarchar(40),
  country nvarchar(40),
  postal_code nvarchar(10),
  phone nvarchar(24),
  email nvarchar(60)
);
CREATE TABLE IF NOT EXISTS genres (
  genre_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  name nvarchar(120)
);
CREATE TABLE IF NOT EXISTS invoice_items (
  invoide_line_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  invoice_id integer NOT NULL,
  track_id integer NOT NULL,
  unit_price numeric(10,2) NOT NULL,
  quantity integer NOT NULL
);
CREATE TABLE IF NOT EXISTS invoices (
  invoice_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  customer_id integer NOT NULL,
  invoice_date datetime NOT NULL,
  billing_address nvarchar(70),
  billing_city nvarchar(40),
  billing_state nvarchar(40),
  billing_country nvarchar(40),
  billing_postal_code nvarchar(10),
  total numeric(10,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS media_types (
  media_type_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  media_name nvarchar(120)
);
CREATE TABLE IF NOT EXISTS playlist_track (
  playlist_id integer NOT NULL,
  track_id integer NOT NULL,
  PRIMARY KEY(playlist_id, track_id)
);
CREATE TABLE IF NOT EXISTS playlists (
  playlist_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  name nvarchar(120)
);
CREATE TABLE IF NOT EXISTS tracks (
  track_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  name nvarchar(200) NOT NULL,
  album_id integer,
  media_type_id integer NOT NULL,
  genre_id integer,
  composer nvarchar(220),
  milliseconds integer NOT NULL,
  bytes integer,
  unit_price numeric(10,2) NOT NULL
);
