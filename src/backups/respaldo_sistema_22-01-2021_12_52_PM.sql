-- MariaDB dump 10.18  Distrib 10.4.16-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: adminpos
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `arqueo_caja`
--

DROP TABLE IF EXISTS `arqueo_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arqueo_caja` (
  `id_arqueo` int NOT NULL AUTO_INCREMENT,
  `id_caja` int DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `fecha_inicio` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_fin` datetime DEFAULT NULL,
  `monto_inicial` decimal(10,2) DEFAULT NULL,
  `monto_final` decimal(10,2) DEFAULT NULL,
  `total_ventas` decimal(10,2) DEFAULT NULL,
  `estatus` int DEFAULT '1',
  PRIMARY KEY (`id_arqueo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arqueo_caja`
--

LOCK TABLES `arqueo_caja` WRITE;
/*!40000 ALTER TABLE `arqueo_caja` DISABLE KEYS */;
INSERT INTO `arqueo_caja` VALUES (1,2,26,'2021-01-03 22:26:53','2021-01-04 01:46:29',2000.00,2100.00,100.00,0),(2,2,26,'2021-01-04 02:04:36','2021-01-04 02:20:20',4000.00,4000.00,100.00,0),(3,2,26,'2021-01-04 02:22:37','2021-01-04 02:40:33',5000.00,5000.00,100.00,0),(4,2,26,'2021-01-04 02:42:02','2021-01-04 09:58:10',500.00,640.00,140.00,0),(5,2,26,'2021-01-04 10:02:46','2021-01-04 11:33:57',3000.00,3180.68,181.00,0),(6,2,26,'2021-01-06 16:24:09','2021-01-20 09:04:20',2000.00,2040.00,40.00,0),(7,2,26,'2021-01-21 20:58:14','2021-01-22 02:14:32',3000.00,3100.00,100.00,0),(8,2,26,'2021-01-22 03:37:31','2021-01-22 04:58:41',4000.00,4500.00,500.00,0),(9,2,26,'2021-01-22 05:42:35','2021-01-22 10:06:36',3000.00,3730.00,730.00,0),(10,2,26,'2021-01-22 13:15:22',NULL,400.00,NULL,NULL,1);
/*!40000 ALTER TABLE `arqueo_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bitacoras`
--

DROP TABLE IF EXISTS `bitacoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bitacoras` (
  `idBitacora` int NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `idUsuario` int DEFAULT NULL,
  `accion` varchar(200) DEFAULT NULL,
  `tabla` varchar(100) DEFAULT NULL,
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idBitacora`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacoras`
--

LOCK TABLES `bitacoras` WRITE;
/*!40000 ALTER TABLE `bitacoras` DISABLE KEYS */;
/*!40000 ALTER TABLE `bitacoras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cajas`
--

DROP TABLE IF EXISTS `cajas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cajas` (
  `id_caja` int NOT NULL AUTO_INCREMENT,
  `numero_caja` varchar(20) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `correlativo` int DEFAULT '1',
  `activo` tinyint DEFAULT '1',
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `asignado` tinyint DEFAULT '0',
  PRIMARY KEY (`id_caja`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='Almacena las cajas del punto de venta';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cajas`
--

LOCK TABLES `cajas` WRITE;
/*!40000 ALTER TABLE `cajas` DISABLE KEYS */;
INSERT INTO `cajas` VALUES (1,'23','Caja miraflores',1,1,'2020-12-14 18:27:08',0),(2,'12','CAJA CENTRO',3,1,'2020-12-14 18:29:13',0);
/*!40000 ALTER TABLE `cajas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoriasproducto`
--

DROP TABLE IF EXISTS `categoriasproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categoriasproducto` (
  `idCategoriasProducto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `fechaCreacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint DEFAULT '1',
  PRIMARY KEY (`idCategoriasProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='categorias de productos, 1 es activo y 0 es inactivo';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoriasproducto`
--

LOCK TABLES `categoriasproducto` WRITE;
/*!40000 ALTER TABLE `categoriasproducto` DISABLE KEYS */;
INSERT INTO `categoriasproducto` VALUES (1,'Físico','2020-11-05 06:00:00',1),(2,'Electrodomestico','2020-11-05 21:48:18',1),(3,'Cereales','2020-11-21 04:22:41',0),(4,'Lacteos','2020-11-21 04:59:01',1),(6,'prueba 3','2020-11-21 05:12:54',0),(7,'Sin categoria','2020-11-21 05:42:33',0),(8,'restriccion','2020-11-21 05:46:46',0),(9,'Bebidas','2020-11-21 09:11:12',1),(10,'PAPELERIA','2020-11-21 20:31:46',1),(11,'Juguetes','2020-12-20 05:49:53',1),(12,'Farmacéutico ','2021-01-09 02:02:28',1),(13,'Cuidado personal','2021-01-09 02:29:10',1),(14,'Limpieza','2021-01-09 02:33:00',1);
/*!40000 ALTER TABLE `categoriasproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `idClientes` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `fechaCreacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `telefono` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `activo` tinyint DEFAULT '1',
  `imagen` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idClientes`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'marco rodriguez','2020-12-13 19:01:00','23342322','prueba@gmail.com','23345 col. miraflores, Tegucigalpa',1,NULL),(2,'andrea cano','2020-12-13 20:43:33','99003456','prueba23@gmail.com','Sps, Honduras',1,NULL),(3,'Mariela paz','2020-12-13 20:45:52','34562345','ejemplo2@gmail.com','otra direccion ',1,NULL),(4,'Alejandro perez','2020-12-13 20:46:19','34234569','ejemplo3@gmail.com','ejemplo 3 dir',0,NULL),(7,'Publico General ','2020-12-22 07:59:08',NULL,NULL,'Honduras',1,NULL),(15,'Online','2021-01-05 19:38:55','22222222','online@gmail.com','Honduras',1,NULL);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compras` (
  `idCompras` int NOT NULL AUTO_INCREMENT,
  `total` decimal(10,2) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `usuario` int DEFAULT NULL,
  `idProveedor` int DEFAULT NULL,
  `idFormaPago` int DEFAULT NULL,
  `activo` tinyint DEFAULT '1',
  `folio` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idCompras`),
  KEY `fk_idFormaPago_idx` (`idFormaPago`),
  KEY `fk_idProveedor_idx` (`idProveedor`),
  KEY `fk_idUsuario_idx` (`usuario`),
  CONSTRAINT `fk_compra_usuario` FOREIGN KEY (`usuario`) REFERENCES `usuarios` (`idUsuarios`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_idFormaPagoCompra` FOREIGN KEY (`idFormaPago`) REFERENCES `formasdepago` (`idFormasDePago`) ON UPDATE CASCADE,
  CONSTRAINT `fk_idProveedorCompra` FOREIGN KEY (`idProveedor`) REFERENCES `proveedores` (`idProveedores`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (58,960.00,'2021-01-22 05:41:54',26,2,1,1,'5689c59c-4371-45ca-8e8f-8a279280979b'),(59,470.00,'2021-01-22 10:31:06',26,1,1,1,'284e1e76-f309-4ec7-8922-5670889edae2'),(60,2400.00,'2021-01-22 13:18:39',26,1,1,1,'e7c26f57-093a-483e-80a1-6f352fe8a3e1');
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detallescompra`
--

DROP TABLE IF EXISTS `detallescompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detallescompra` (
  `idDetallesCompra` int NOT NULL AUTO_INCREMENT,
  `idCompra` int DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `nombre` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idDetallesCompra`),
  KEY `fk_idCompra_idx` (`idCompra`),
  KEY `fk_idProducto_idx` (`idProducto`),
  CONSTRAINT `fk_idCompraDetalleCompra` FOREIGN KEY (`idCompra`) REFERENCES `compras` (`idCompras`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_idProductoDetalleCompra` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProductos`) ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallescompra`
--

LOCK TABLES `detallescompra` WRITE;
/*!40000 ALTER TABLE `detallescompra` DISABLE KEYS */;
INSERT INTO `detallescompra` VALUES (1,58,45,96.00,10,'2021-01-22 05:41:54','Lysol '),(2,59,48,47.00,10,'2021-01-22 10:31:06','Prueba'),(3,60,46,120.00,20,'2021-01-22 13:18:40','Mascarilla quirúrgica');
/*!40000 ALTER TABLE `detallescompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detallesventa`
--

DROP TABLE IF EXISTS `detallesventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detallesventa` (
  `idDetalleVenta` int NOT NULL AUTO_INCREMENT,
  `idVenta` int DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `nombre` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idDetalleVenta`),
  KEY `fk_idventa_idx` (`idVenta`),
  KEY `fk_idProducto_idx` (`idProducto`),
  CONSTRAINT `fk_idProducto` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProductos`) ON UPDATE CASCADE,
  CONSTRAINT `fk_idventa` FOREIGN KEY (`idVenta`) REFERENCES `ventas` (`idVentas`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallesventa`
--

LOCK TABLES `detallesventa` WRITE;
/*!40000 ALTER TABLE `detallesventa` DISABLE KEYS */;
INSERT INTO `detallesventa` VALUES (1,50,45,130.00,5,'2021-01-22 05:42:54','Lysol '),(2,51,48,40.00,2,'2021-01-22 10:36:08','Prueba'),(3,52,46,240.00,2,'2021-01-22 13:17:04','Mascarilla quirúrgica'),(4,52,38,100.00,3,'2021-01-22 13:17:04','Gel antibacterial');
/*!40000 ALTER TABLE `detallesventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresas` (
  `idEmpresas` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `fechaCreacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `RTN` varchar(14) DEFAULT NULL,
  `saludo` varchar(200) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idEmpresas`),
  UNIQUE KEY `RTN_UNIQUE` (`RTN`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

LOCK TABLES `empresas` WRITE;
/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'POS11','95246871','75c84287-5cd1-11eb-8892-94659c30abd3.png','Tegucigalpa','2020-12-14 00:34:03','08012002234232','Gracias por su compra, lo esperamos pronto','denisvsnew@gmail.com');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `formasdepago`
--

DROP TABLE IF EXISTS `formasdepago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formasdepago` (
  `idFormasDePago` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) DEFAULT NULL,
  `fechaCreacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint DEFAULT '1',
  PRIMARY KEY (`idFormasDePago`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='Guarda formas de pago aceptadas en el POS';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formasdepago`
--

LOCK TABLES `formasdepago` WRITE;
/*!40000 ALTER TABLE `formasdepago` DISABLE KEYS */;
INSERT INTO `formasdepago` VALUES (1,'Efectivo','2020-12-17 07:39:29',1),(2,'Tarjeta visa','2021-01-22 04:31:46',1),(3,'Tarjeta Mastercar','2021-01-22 04:34:17',1),(4,'Cheque','2021-01-22 04:35:26',0);
/*!40000 ALTER TABLE `formasdepago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventarios`
--

DROP TABLE IF EXISTS `inventarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventarios` (
  `idInventarios` int NOT NULL AUTO_INCREMENT,
  `producto` varchar(100) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `fechaCreacion` date DEFAULT NULL,
  `proveedor` varchar(100) DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  PRIMARY KEY (`idInventarios`),
  KEY `fk_productoInventario_idx` (`idProducto`),
  CONSTRAINT `fk_productoInventario` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProductos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventarios`
--

LOCK TABLES `inventarios` WRITE;
/*!40000 ALTER TABLE `inventarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `evento` varchar(100) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `ip` varchar(20) DEFAULT NULL,
  `detalles` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,26,'Cierre de sesión','2021-01-22 05:40:07','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(2,26,'Inicio de sesion ','2021-01-22 05:40:34','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(3,26,'Inicio de sesion ','2021-01-22 09:28:02','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(4,33,'Inicio de sesion ','2021-01-22 10:02:00','127.0.0.1',NULL),(5,33,'Cierre de sesión','2021-01-22 10:02:07','127.0.0.1',NULL),(6,26,'Inicio de sesion ','2021-01-22 10:13:07','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(7,26,'Inicio de sesion ','2021-01-22 12:53:00','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(8,26,'Cierre de sesión','2021-01-22 13:07:59','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(9,26,'Inicio de sesion ','2021-01-22 13:12:00','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenes_online`
--

DROP TABLE IF EXISTS `ordenes_online`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordenes_online` (
  `id_orden` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `nombre_cliente` varchar(100) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `codigo_postal` varchar(45) DEFAULT NULL,
  `detalle` varchar(300) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `costo_envio` decimal(10,2) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint DEFAULT '0',
  `id_venta` int DEFAULT NULL,
  PRIMARY KEY (`id_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_online`
--

LOCK TABLES `ordenes_online` WRITE;
/*!40000 ALTER TABLE `ordenes_online` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordenes_online` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos` (
  `idProductos` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `fechaCreacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `precio_venta` decimal(10,2) DEFAULT NULL,
  `activo` tinyint DEFAULT '1',
  `idCategoria` int DEFAULT NULL,
  `codigo` varchar(40) DEFAULT NULL,
  `precio_compra` decimal(10,2) DEFAULT '0.00',
  `existencias` int DEFAULT '0',
  `stock_min` int DEFAULT '0',
  `inventariable` tinyint DEFAULT NULL,
  `id_unidad` int DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `picture` varchar(200) DEFAULT NULL,
  `codigo_qr` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idProductos`),
  KEY `fk_idCategoria_idx` (`idCategoria`),
  KEY `fk_producto_unidad_idx` (`id_unidad`),
  CONSTRAINT `fk_idCategoriaProducto` FOREIGN KEY (`idCategoria`) REFERENCES `categoriasproducto` (`idCategoriasProducto`),
  CONSTRAINT `fk_producto_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidades` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (36,'Caja de leche ','2020-12-27 17:53:38',18.60,1,9,'L128',10.00,0,10,1,3,'Litro de leche en caja de larga duración','bd45b657-489e-11eb-a8d4-94659c30abd3.png','bd4331c8-489e-11eb-8943-94659c30abd3.png'),(37,'Alcohol etílico ','2021-01-08 20:06:24',40.00,1,12,'01',30.50,79,20,1,7,'Bote de alcohol etílico 70 grados de 1000 ml.','465ba4bf-521f-11eb-9b9a-94659c30abd3.jpg','45da75e6-521f-11eb-9227-94659c30abd3.png'),(38,'Gel antibacterial','2021-01-08 20:08:22',100.00,1,12,'02',80.00,787,20,1,7,'Bote de gel antibacterial, con 70% de alcohol. ','8cefc3b9-521f-11eb-aad3-94659c30abd3.jpg','8cef9d77-521f-11eb-a0f0-94659c30abd3.png'),(39,'Agua oxigenada','2021-01-08 20:10:21',50.00,1,12,'03',43.00,195,20,1,7,'Bote de agua oxigenada, presentación de 500 ml, marca H.E.B.','cf5acd04-5ca7-11eb-b9ff-94659c30abd3.jpg','d3ad3026-521f-11eb-92c0-94659c30abd3.png'),(40,'Curas','2021-01-08 20:13:01',35.00,1,12,'04',27.50,17,15,1,8,'Caja de 50 curas o vendas medicas impermeables, marca CureBand.','33234e76-5220-11eb-a8a9-94659c30abd3.png','33230058-5220-11eb-9af2-94659c30abd3.png'),(41,'Esparadrapo ','2021-01-08 20:24:04',10.00,1,12,'05',6.30,500,20,1,9,'Esparadrapo medico marca M3, para uso medico y casero.','46d59356-5ca8-11eb-9a0e-94659c30abd3.jpg','be435f3b-5221-11eb-8a7d-94659c30abd3.png'),(42,'Algodón medico ','2021-01-08 20:25:59',40.00,1,12,'06',34.00,20,30,1,5,'Paquete de algodón para uso medico y casero, marca RBG.','02f933d3-5222-11eb-acbc-94659c30abd3.webp','02f8bf88-5222-11eb-97d3-94659c30abd3.png'),(43,'Mascarilla N95','2021-01-08 20:27:27',50.00,1,12,'07',38.30,40,60,1,9,'Mascarilla N95 unidad, marca 3M.','3793e9a5-5222-11eb-ba9b-94659c30abd3.png','37937556-5222-11eb-946a-94659c30abd3.png'),(44,'Papel higiénico','2021-01-08 20:31:49',130.00,1,13,'08',95.00,29,30,1,5,'Paquete de papel higiénico, 12 rollos doble hoja, marca premier.','d3467cbd-5222-11eb-b94f-94659c30abd3.webp','d346079a-5222-11eb-8e11-94659c30abd3.png'),(45,'Lysol ','2021-01-08 20:34:18',130.00,1,14,'09',96.00,33,30,1,7,'Bote de desinfectante en aerosol Lysol, presentacion de 400 ml.','2c7aea7d-5223-11eb-8906-94659c30abd3.jpg','2c7a7545-5223-11eb-8b84-94659c30abd3.png'),(46,'Mascarilla quirúrgica','2021-01-08 20:36:10',240.00,1,12,'10',120.00,18,30,1,5,'Caja de mascarillas quirúrgica, 20 unidades color azul.','6f063498-5223-11eb-8d7f-94659c30abd3.jpg','6f05c065-5223-11eb-99b4-94659c30abd3.png'),(47,'prueba 23445556','2021-01-20 08:59:53',23.00,0,1,'777',30.00,0,20,1,1,'prueba','26f38c03-5b30-11eb-9769-94659c30abd3.jpg','26ad6af4-5b30-11eb-8c08-94659c30abd3.png'),(48,'Prueba','2021-01-22 10:22:49',40.00,1,14,'12',47.00,8,10,1,5,'Prueba de producto','11cd49d5-5cce-11eb-a1a7-94659c30abd3.jpg','11aac6ac-5cce-11eb-8b1e-94659c30abd3.png');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proveedores` (
  `idProveedores` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `fechaCreacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `telefono` varchar(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `estado` tinyint DEFAULT '1',
  `direccion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idProveedores`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Plasticos estrella ','2021-01-21 10:46:39','23223490','plast@gmail.com',1,'Tegucigalpa 12345'),(2,'Variedades garcia','2021-01-21 12:03:03','34567888','garcias@yahoo.com',1,'Calle real, no. 3456, Comayagüela '),(4,'Mercadeo','2021-01-22 03:45:27',NULL,NULL,1,'Honduras');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `respaldos`
--

DROP TABLE IF EXISTS `respaldos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `respaldos` (
  `idrespaldos` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idrespaldos`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respaldos`
--

LOCK TABLES `respaldos` WRITE;
/*!40000 ALTER TABLE `respaldos` DISABLE KEYS */;
INSERT INTO `respaldos` VALUES (1,'respaldo_sistema_20-01-2021_08_AM_37.sql',26,'2021-01-20 08:37:47'),(2,'respaldo_sistema_20-01-2021_09_04_AM.sql',26,'2021-01-21 00:14:59'),(3,'respaldo_sistema_21-01-2021_09_18_PM.sql',26,'2021-01-21 21:18:59'),(4,'respaldo_sistema_22-01-2021_12_52_PM.sql',26,'2021-01-22 13:27:11');
/*!40000 ALTER TABLE `respaldos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temporal_compra`
--

DROP TABLE IF EXISTS `temporal_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temporal_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `folio` varchar(100) DEFAULT NULL,
  `id_producto` int DEFAULT NULL,
  `codigo` varchar(20) DEFAULT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='Almacenar compras temporal sin grabar.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temporal_compra`
--

LOCK TABLES `temporal_compra` WRITE;
/*!40000 ALTER TABLE `temporal_compra` DISABLE KEYS */;
/*!40000 ALTER TABLE `temporal_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades`
--

DROP TABLE IF EXISTS `unidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `abreviatura` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `activo` tinyint DEFAULT '1',
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `extra2` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='manejo de medidas y unidades de los productos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades`
--

LOCK TABLES `unidades` WRITE;
/*!40000 ALTER TABLE `unidades` DISABLE KEYS */;
INSERT INTO `unidades` VALUES (1,'Libra','LB',1,'2020-11-20 19:28:53',NULL),(2,'Kilogramo','KG',1,'2020-11-20 21:25:47',NULL),(3,'Litro','LT',1,'2020-11-21 03:11:36',NULL),(4,'GRAMOS','G',0,'2020-11-21 14:30:55',NULL),(5,'Paquete','PQ',1,'2020-12-09 20:38:41',NULL),(6,'Sin unidad','SN',1,'2020-12-10 22:41:37',NULL),(7,'Bote','BT',1,'2021-01-08 20:04:03',NULL),(8,'Caja','CJ',1,'2021-01-08 20:11:02',NULL),(9,'Unidad','UNI',1,'2021-01-08 20:22:58',NULL),(10,'Prueba','PA',0,'2021-01-22 05:09:25',NULL);
/*!40000 ALTER TABLE `unidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `idUsuarios` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `estado` varchar(20) DEFAULT 'activo',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(60) NOT NULL,
  `password` varchar(200) NOT NULL,
  `telefono` varchar(200) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `profilepicture` varchar(200) DEFAULT NULL,
  `id_caja` int DEFAULT NULL,
  `token` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idUsuarios`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_usuario_caja_idx` (`id_caja`),
  CONSTRAINT `fk_usuario_caja` FOREIGN KEY (`id_caja`) REFERENCES `cajas` (`id_caja`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='relacion de cajas con usuarios';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (26,'Denis Vasquez','admin','activo','2020-11-20 02:36:55','denisvsnew@gmail.com','$2b$12$bYenmtbJF5gOg2sal8kR7.0dJ7uZ4ynRQ1KijUzIqwXwMciWxURQ.','85246871','Tegucigalpa, Honduras','e39f16ce-3acc-11eb-8f59-94659c30abd3.png',2,'ImRlbmlzdnNuZXdAZ21haWwuY29tIg.YAogAg.xoT--1XWHLCS1kKOODmljD7rqAg'),(30,'pablo 1','usuario','activo','2020-12-15 11:15:49','pablo1@gmail.com','$2b$12$STA4R.VK5fKNgyxX4FMSEe2pYdTNaXHV0xA1NlV70d8ZdBooq97t.','34999444','None','imagen-no-disponible.jpg',NULL,NULL),(33,'Maria Castro','usuario','activo','2021-01-22 09:55:17','mcastro@gmail.com','$2b$12$9YDurYAvKrnnoKXIAKVT2.AnV0JemlIL04KjMEvVu9wrnL3hUrM7e',NULL,NULL,NULL,NULL,NULL),(34,'prueba','usuario','activo','2021-01-22 13:10:32','prueba@gmail.com','$2b$12$JuPlWGB3FmefYeA.iCbrze02LiZXUhPfXrdYgv6raozlMOVBzDRwK',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas` (
  `idVentas` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) DEFAULT NULL,
  `usuario` int DEFAULT NULL,
  `idCliente` int DEFAULT NULL,
  `activo` tinyint DEFAULT '1',
  `idFormaPago` int DEFAULT NULL,
  `folio` varchar(100) DEFAULT NULL,
  `id_caja` int DEFAULT NULL,
  `id_arqueo` int DEFAULT NULL,
  `tipo_venta` int DEFAULT NULL,
  PRIMARY KEY (`idVentas`),
  KEY `fk_idCliente_idx` (`idCliente`),
  KEY `fk_idUsuario_idx` (`usuario`),
  KEY `fk_idFormaPago_idx` (`idFormaPago`),
  KEY `fk_caja_venta_idx` (`id_caja`),
  CONSTRAINT `fk_idClienteVenta` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idClientes`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_idFormaPagoVenta` FOREIGN KEY (`idFormaPago`) REFERENCES `formasdepago` (`idFormasDePago`),
  CONSTRAINT `fk_idUsuarioVenta` FOREIGN KEY (`usuario`) REFERENCES `usuarios` (`idUsuarios`) ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (50,'2021-01-22 05:42:54',650.00,26,7,1,1,'19',2,9,NULL),(51,'2021-01-22 10:36:07',80.00,26,7,1,1,'20',2,9,NULL),(52,'2021-01-22 13:17:03',780.00,26,1,1,1,'2',2,10,NULL);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-22 13:27:17
