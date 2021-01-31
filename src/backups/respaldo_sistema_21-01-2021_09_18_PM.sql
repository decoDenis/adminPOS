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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arqueo_caja`
--

LOCK TABLES `arqueo_caja` WRITE;
/*!40000 ALTER TABLE `arqueo_caja` DISABLE KEYS */;
INSERT INTO `arqueo_caja` VALUES (1,2,26,'2021-01-03 22:26:53','2021-01-04 01:46:29',2000.00,2100.00,100.00,0),(2,2,26,'2021-01-04 02:04:36','2021-01-04 02:20:20',4000.00,4000.00,100.00,0),(3,2,26,'2021-01-04 02:22:37','2021-01-04 02:40:33',5000.00,5000.00,100.00,0),(4,2,26,'2021-01-04 02:42:02','2021-01-04 09:58:10',500.00,640.00,140.00,0),(5,2,26,'2021-01-04 10:02:46','2021-01-04 11:33:57',3000.00,3180.68,181.00,0),(6,2,26,'2021-01-06 16:24:09','2021-01-20 09:04:20',2000.00,2040.00,40.00,0),(7,2,26,'2021-01-21 20:58:14',NULL,3000.00,NULL,NULL,1);
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
INSERT INTO `cajas` VALUES (1,'23','Caja miraflores',1,1,'2020-12-14 18:27:08',0),(2,'12','CAJA CENTRO',17,1,'2020-12-14 18:29:13',0);
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
INSERT INTO `categoriasproducto` VALUES (1,'Fisico','2020-11-05 06:00:00',1),(2,'Electrodomestico','2020-11-05 21:48:18',1),(3,'Cereales','2020-11-21 04:22:41',0),(4,'Lacteos','2020-11-21 04:59:01',1),(5,'nueva prueba','2020-11-21 05:10:21',0),(6,'prueba 3','2020-11-21 05:12:54',0),(7,'Sin categoria','2020-11-21 05:42:33',0),(8,'restriccion','2020-11-21 05:46:46',1),(9,'Bebidas','2020-11-21 09:11:12',1),(10,'PAPELERIA','2020-11-21 20:31:46',1),(11,'Juguetes','2020-12-20 05:49:53',1),(12,'Farmacéutico ','2021-01-09 02:02:28',1),(13,'Cuidado personal','2021-01-09 02:29:10',1),(14,'Limpieza','2021-01-09 02:33:00',1);
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
INSERT INTO `clientes` VALUES (1,'marco rodriguez','2020-12-13 19:01:00','23342322','prueba@gmail.com','23345 col. miraflores, Tegucigalpa',1,NULL),(2,'andrea cano','2020-12-13 20:43:33','99003456','prueba23@gmail.com','Sps, Honduras',1,NULL),(3,'Mariela paz','2020-12-13 20:45:52','34562345','ejemplo2@gmail.com','otra direccion ',1,NULL),(4,'Alejandro perez','2020-12-13 20:46:19','34234569','ejemplo3@gmail.com','ejemplo 3 dir',0,NULL),(5,'Prueba ','2020-12-19 10:01:23','22222222','prueba1@gmail.com','honduras',1,NULL),(6,'prueba 2 ','2020-12-19 10:01:46','22222222','prueb2@gmail.com','honduras',0,NULL),(7,'Publico General ','2020-12-22 07:59:08',NULL,NULL,'Honduras',1,NULL),(15,'Online','2021-01-05 19:38:55','22222222','online@gmail.com','Honduras',1,NULL),(16,'cliente de prueba ','2021-01-21 12:48:12','34234532','prueba34@yahoo.com','Tegucigalpa, Honduras',0,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (10,69.00,'2020-12-17 10:09:18',26,NULL,1,1,'bebd0d32-b844-4b9f-b393-aaba8f8c94cf'),(11,23.00,'2020-12-17 10:15:17',26,NULL,1,1,'ae921444-8f4a-4679-bb7c-6143764615b1'),(12,23.00,'2020-12-17 10:20:10',26,NULL,1,1,'e7016489-7e92-4eb7-a01d-5fd9d8870257'),(13,23.00,'2020-12-17 10:21:23',26,NULL,1,1,'929d549d-b42c-4da3-b36a-d402ba4a6da7'),(14,23.00,'2020-12-17 10:25:20',26,NULL,1,1,'f5e8526b-fdb6-484f-8e00-00752796f923'),(15,23.00,'2020-12-17 10:34:55',26,NULL,1,1,'d77325fe-e58b-41de-a527-773f01a92770'),(16,23.00,'2020-12-17 10:45:20',26,NULL,1,1,'041a3981-26e6-403d-b8ed-07dc7e4db533'),(17,23.00,'2020-12-17 10:49:07',26,NULL,1,1,'8640b0f1-fd79-48ba-bb20-95d2553ab6c4'),(18,23.00,'2020-12-17 11:05:14',26,NULL,1,1,'b77fae9d-c609-414c-ac1c-21ba80cbe85b'),(19,1150.00,'2020-12-17 11:09:39',26,NULL,1,1,'ba0fc5f9-3339-4fab-ae99-9448de48f81b'),(20,71.00,'2020-12-17 11:12:39',26,NULL,1,1,'e307bbc7-9a93-4e93-a427-f5535badf61b'),(21,23.00,'2020-12-17 11:13:33',26,NULL,1,1,'f875076f-7147-4983-9435-01a65c9feaa3'),(22,1150.00,'2020-12-17 11:16:44',26,NULL,1,1,'790b3bba-25f5-4e81-a2a1-f926a7d2edba'),(23,460.00,'2020-12-17 11:23:09',26,NULL,1,1,'f9d5b48e-fce7-4e86-b6e5-6f24f1f73f5d'),(24,1380.00,'2020-12-17 11:24:08',26,NULL,1,1,'89211a21-42cf-4d6f-b8c2-068cab6e06f2'),(25,23.00,'2020-12-17 11:24:47',26,NULL,1,1,'b76045a3-9251-4927-8bd1-050af280374f'),(26,1150.00,'2020-12-17 11:27:46',26,NULL,1,1,'31f886c7-8531-478c-88a9-10c8e34312ba'),(27,1035.00,'2020-12-17 11:30:03',26,NULL,1,1,'2753214e-d1e5-478d-b3e5-82db8d347a7a'),(28,920.00,'2020-12-17 11:31:46',26,NULL,1,1,'c49c421f-ee02-4934-aedd-f9eaac68a77b'),(29,460.00,'2020-12-17 11:39:16',26,NULL,1,1,'f3bee2d5-70fa-4c95-a67a-58396470554d'),(30,2300.00,'2020-12-17 11:47:02',26,NULL,1,1,'81879183-4df8-44b3-a8a7-4b733753f5eb'),(31,1150.00,'2020-12-17 13:19:38',26,NULL,1,1,'5c31237e-72e2-41f2-a080-f6bc00fca46f'),(32,12000.00,'2020-12-17 18:40:01',26,NULL,1,1,'0c6f82a1-5374-4977-9287-abbf5ef881d0'),(33,20.00,'2020-12-17 19:03:32',26,NULL,1,1,'3362a3bd-533f-4250-9a72-856241a89239'),(34,575.10,'2020-12-18 15:11:07',26,NULL,1,1,'1960b441-1612-4a7f-a75b-47a529d3100a'),(35,868.70,'2020-12-18 15:12:53',26,NULL,1,1,'291062fc-64d7-47d8-b221-bb38c68dff50'),(36,1043.41,'2020-12-18 17:55:39',26,NULL,1,1,'712f785a-f419-4d14-b223-8e32102326eb'),(37,1220.68,'2020-12-19 03:10:28',26,NULL,1,1,'a33156fb-de82-45e6-bc3d-cea1b68b09b8'),(38,24023.00,'2020-12-19 17:22:47',26,NULL,1,1,'5c8af787-c47d-4279-b701-fff20e7af25d'),(39,24978.00,'2020-12-24 02:36:16',26,NULL,1,1,'bbba5d19-8bdd-42b4-854c-21a3a22a332e'),(40,80000.00,'2020-12-27 13:17:01',26,NULL,1,0,'ac625131-08cc-4e44-92ca-72fb4e3486e7'),(41,300000.00,'2020-12-27 13:19:22',26,NULL,1,1,'2cfb3e10-73c1-435e-847a-d43c36768f8f'),(42,230.00,'2021-01-04 02:23:13',26,NULL,1,1,'c0bd55a4-b55f-48af-82a7-0d9fd48d0438'),(43,2300000.00,'2021-01-04 02:23:59',26,NULL,1,0,'bdbb0908-5b2f-47fa-a704-5bbccf9a27e2'),(44,2440.00,'2021-01-08 23:05:09',26,NULL,1,1,'70ba85cd-df06-4493-82ef-b3e84b92a330'),(45,75750.00,'2021-01-08 23:17:28',26,NULL,1,1,'f73d1190-d3df-46c9-8d7a-4e6facf99321'),(46,86.00,'2021-01-21 20:55:56',26,NULL,1,1,'68a74201-3aa5-465a-8145-53c171f9f298'),(47,129.00,'2021-01-21 20:57:22',26,NULL,1,1,'f9eddbc8-c1e2-48ac-bc41-7d5d39d90a26');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallescompra`
--

LOCK TABLES `detallescompra` WRITE;
/*!40000 ALTER TABLE `detallescompra` DISABLE KEYS */;
INSERT INTO `detallescompra` VALUES (1,29,10,23.00,20,'2020-12-17 11:39:16','Caja de carton armable'),(2,30,10,23.00,100,'2020-12-17 11:47:02','Caja de carton armable'),(3,31,10,23.00,50,'2020-12-17 13:19:38','Caja de carton armable'),(4,32,3,12.00,1000,'2020-12-17 18:40:01','Refresco coca cola'),(5,33,3,12.00,1,'2020-12-17 19:03:32','Refresco coca cola'),(6,33,4,8.00,1,'2020-12-17 19:03:33','queso'),(7,34,28,23.20,3,'2020-12-18 15:11:08','probando producto 4'),(8,34,10,23.00,3,'2020-12-18 15:11:09','Caja de carton armable'),(9,34,27,87.30,5,'2020-12-18 15:11:09','probando producto 3 '),(10,35,25,20.09,30,'2020-12-18 15:12:54','nuevo producto probando '),(11,35,10,23.00,10,'2020-12-18 15:12:54','Caja de carton armable'),(12,35,3,12.00,3,'2020-12-18 15:12:55','Refresco coca cola'),(13,36,10,23.00,1,'2020-12-18 17:55:39','Caja de carton armable'),(14,36,3,12.00,3,'2020-12-18 17:55:39','Refresco coca cola'),(15,36,25,20.09,49,'2020-12-18 17:55:40','nuevo producto probando '),(16,37,10,30.00,23,'2020-12-19 03:10:28','Caja de carton armable'),(17,37,3,20.00,23,'2020-12-19 03:10:29','Refresco coca cola'),(18,37,25,23.56,3,'2020-12-19 03:10:29','nuevo producto probando '),(19,38,10,23.00,1,'2020-12-19 17:22:47','Caja de carton armable'),(20,38,3,12.00,2000,'2020-12-19 17:22:48','Refresco coca cola'),(21,39,10,23.00,1086,'2020-12-24 02:36:16','Caja de carton armable'),(22,40,32,400.00,200,'2020-12-27 13:17:01','ROBOT'),(23,41,31,10000.00,30,'2020-12-27 13:19:22','Monitor'),(24,42,10,23.00,10,'2021-01-04 02:23:13','Caja de carton armable'),(25,43,10,23.00,100000,'2021-01-04 02:23:59','Caja de carton armable'),(26,44,37,30.50,80,'2021-01-08 23:05:09','Alcohol etílico '),(27,45,39,43.00,200,'2021-01-08 23:17:28','Agua oxigenada'),(28,45,41,6.30,500,'2021-01-08 23:17:28','Esparadrapo '),(29,45,38,80.00,800,'2021-01-08 23:17:29','Gel antibacterial'),(30,46,39,43.00,2,'2021-01-21 20:55:57','Agua oxigenada'),(31,47,39,43.00,3,'2021-01-21 20:57:22','Agua oxigenada');
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
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallesventa`
--

LOCK TABLES `detallesventa` WRITE;
/*!40000 ALTER TABLE `detallesventa` DISABLE KEYS */;
INSERT INTO `detallesventa` VALUES (1,3,3,20.00,82,'2020-12-19 03:45:09','Refresco coca cola'),(2,4,3,20.00,100,'2020-12-19 09:03:31','Refresco coca cola'),(3,5,10,30.00,5,'2020-12-21 21:54:56','Caja de carton armable'),(4,6,10,30.00,2,'2020-12-22 00:01:46','Caja de carton armable'),(5,6,3,20.00,4,'2020-12-22 00:01:47','Refresco coca cola'),(6,6,28,23.34,1,'2020-12-22 00:01:48','probando producto 4'),(7,6,27,102.20,3,'2020-12-22 00:01:48','probando producto 3 '),(8,7,10,30.00,200,'2020-12-22 00:10:49','Caja de carton armable'),(9,8,10,30.00,20,'2020-12-22 00:13:50','Caja de carton armable'),(10,9,10,30.00,3,'2020-12-22 07:49:00','Caja de carton armable'),(11,10,10,30.00,3,'2020-12-22 08:01:49','Caja de carton armable'),(12,11,10,30.00,2,'2020-12-22 10:49:13','Caja de carton armable'),(13,12,10,30.00,2,'2020-12-22 10:55:53','Caja de carton armable'),(14,13,10,30.00,2,'2020-12-22 11:31:46','Caja de carton armable'),(15,14,10,30.00,1,'2020-12-23 12:01:49','Caja de carton armable'),(16,15,10,30.00,1,'2020-12-24 01:43:17','Caja de carton armable'),(17,16,10,30.00,844,'2020-12-24 02:21:41','Caja de carton armable'),(18,17,10,30.00,44,'2020-12-24 02:30:24','Caja de carton armable'),(19,18,10,30.00,44,'2020-12-24 02:32:02','Caja de carton armable'),(20,19,10,30.00,1,'2020-12-24 02:37:30','Caja de carton armable'),(21,20,3,20.00,4,'2020-12-26 16:00:00','Refresco coca cola'),(22,21,3,20.00,40,'2020-12-27 02:06:28','Refresco coca cola'),(23,23,3,20.00,1,'2020-12-29 13:53:17','Refresco coca cola'),(24,24,3,20.00,1,'2020-12-30 01:21:31','Refresco coca cola'),(25,24,32,300.00,2,'2020-12-30 01:21:31','ROBOT'),(26,25,32,300.00,2,'2020-12-30 01:23:46','ROBOT'),(27,26,3,20.00,5,'2021-01-04 01:20:26','Refresco coca cola'),(28,27,10,30.00,4,'2021-01-04 02:42:23','Caja de carton armable'),(29,28,3,20.00,1,'2021-01-04 09:58:36','Refresco coca cola'),(30,29,3,20.00,1,'2021-01-04 10:41:21','Refresco coca cola'),(31,30,10,30.00,3,'2021-01-04 10:41:48','Caja de carton armable'),(32,31,25,23.56,3,'2021-01-04 10:42:30','nuevo producto probando '),(33,34,32,300.00,1,'2021-01-05 19:42:43','ROBOT'),(34,35,32,300.00,1,'2021-01-05 19:45:19','ROBOT'),(35,36,32,300.00,1,'2021-01-05 19:53:42','ROBOT'),(36,37,32,300.00,1,'2021-01-05 20:15:08','ROBOT'),(37,38,3,20.00,3,'2021-01-06 16:29:22','Refresco coca cola'),(38,38,10,30.00,1,'2021-01-06 16:29:22','Caja de carton armable'),(39,39,3,20.00,3,'2021-01-06 16:29:23','Refresco coca cola'),(40,39,10,30.00,1,'2021-01-06 16:29:23','Caja de carton armable'),(41,40,37,40.00,3,'2021-01-08 21:21:35','Alcohol etílico '),(42,41,10,30.00,20000,'2021-01-08 23:11:31','Caja de carton armable'),(43,42,37,40.00,1,'2021-01-20 08:55:49','Alcohol etílico '),(44,43,38,100.00,1,'2021-01-21 20:16:41','Gel antibacterial'),(45,43,45,130.00,1,'2021-01-21 20:16:42','Lysol '),(46,44,39,50.00,5,'2021-01-21 20:58:53','Agua oxigenada'),(47,45,39,50.00,5,'2021-01-21 21:03:06','Agua oxigenada'),(48,46,38,100.00,3,'2021-01-21 21:05:33','Gel antibacterial');
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
INSERT INTO `empresas` VALUES (1,'puesto23','95246871','8bb273f0-47a3-11eb-bb55-94659c30abd3.png','Tegucigalpa','2020-12-14 00:34:03','08012002234232','Gracias por su compra, lo esperamos pronto','denisvsnew@gmail.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Guarda formas de pago aceptadas en el POS';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formasdepago`
--

LOCK TABLES `formasdepago` WRITE;
/*!40000 ALTER TABLE `formasdepago` DISABLE KEYS */;
INSERT INTO `formasdepago` VALUES (1,'Efectivo','2020-12-17 07:39:29',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (2,26,'Cierre de sesión','2020-12-19 11:33:55','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(3,26,'Inicio de sesion ','2020-12-19 11:34:24','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(4,26,'Cierre de sesión','2020-12-19 11:44:37','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(5,26,'Inicio de sesion ','2020-12-19 11:44:51','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(6,26,'Cierre de sesión','2020-12-19 17:17:18','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(7,26,'Inicio de sesion ','2020-12-19 17:18:10','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(8,26,'Cierre de sesión','2020-12-19 22:33:57','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(9,26,'Inicio de sesion ','2020-12-19 22:38:51','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(10,26,'Cierre de sesión','2020-12-20 12:42:34','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(11,26,'Inicio de sesion ','2020-12-20 13:07:24','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(12,26,'Cierre de sesión','2020-12-20 23:07:06','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(13,26,'Inicio de sesion ','2020-12-21 11:44:49','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(14,26,'Cierre de sesión','2020-12-21 11:46:15','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(15,26,'Inicio de sesion ','2020-12-21 11:47:23','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(16,26,'Cierre de sesión','2020-12-21 12:04:26','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(17,26,'Inicio de sesion ','2020-12-21 20:08:59','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(18,26,'Cierre de sesión','2020-12-21 22:33:28','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(19,26,'Inicio de sesion ','2020-12-21 22:35:13','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(20,26,'Cierre de sesión','2020-12-22 10:50:42','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(21,26,'Inicio de sesion ','2020-12-22 10:55:28','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(22,26,'Cierre de sesión','2020-12-22 11:27:10','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(23,26,'Inicio de sesion ','2020-12-22 11:28:53','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(24,26,'Inicio de sesion ','2020-12-23 12:01:19','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(25,26,'Cierre de sesión','2020-12-24 01:42:14','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(26,26,'Inicio de sesion ','2020-12-24 01:42:31','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(27,26,'Cierre de sesión','2020-12-24 03:53:07','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(28,26,'Inicio de sesion ','2020-12-26 10:38:46','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(29,26,'Cierre de sesión','2020-12-26 19:17:41','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(30,26,'Inicio de sesion ','2020-12-26 19:18:06','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(31,26,'Cierre de sesión','2020-12-26 20:50:54','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(32,26,'Inicio de sesion ','2020-12-26 20:51:35','127.0.0.1',NULL),(33,26,'Inicio de sesion ','2020-12-26 21:03:29','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(34,26,'Cierre de sesión','2020-12-26 21:09:04','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(35,26,'Inicio de sesion ','2020-12-26 21:22:39','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(36,26,'Cierre de sesión','2020-12-26 21:23:54','127.0.0.1',NULL),(37,26,'Inicio de sesion ','2020-12-26 23:14:18','127.0.0.1',NULL),(38,26,'Cierre de sesión','2020-12-26 23:16:57','127.0.0.1',NULL),(39,26,'Inicio de sesion ','2020-12-26 23:17:14','127.0.0.1',NULL),(40,26,'Cierre de sesión','2020-12-26 23:18:56','127.0.0.1',NULL),(41,26,'Cierre de sesión','2020-12-26 23:25:14','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(42,26,'Inicio de sesion ','2020-12-26 23:25:40','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(43,26,'Inicio de sesion ','2020-12-27 00:13:58','127.0.0.1',NULL),(44,26,'Inicio de sesion ','2020-12-27 00:27:50','127.0.0.1',NULL),(45,26,'Inicio de sesion ','2020-12-27 01:44:08','127.0.0.1',NULL),(46,26,'Inicio de sesion ','2020-12-27 02:19:04','127.0.0.1',NULL),(47,26,'Cierre de sesión','2020-12-27 04:04:16','127.0.0.1',NULL),(48,26,'Cierre de sesión','2020-12-27 04:04:29','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(49,26,'Inicio de sesion ','2020-12-27 13:05:57','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(50,26,'Cierre de sesión','2020-12-28 19:46:59','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(51,26,'Inicio de sesion ','2020-12-28 21:19:06','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(52,26,'Cierre de sesión','2020-12-29 10:24:21','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(53,26,'Inicio de sesion ','2020-12-29 10:34:17','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(54,26,'Cierre de sesión','2020-12-29 13:35:31','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(55,26,'Inicio de sesion ','2020-12-29 13:36:25','127.0.0.1',NULL),(56,26,'Cierre de sesión','2020-12-29 13:54:02','127.0.0.1',NULL),(57,26,'Inicio de sesion ','2020-12-29 23:50:23','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(58,26,'Cierre de sesión','2020-12-30 10:37:14','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(59,26,'Inicio de sesion ','2021-01-03 20:13:51','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(60,26,'Cierre de sesión','2021-01-04 03:27:02','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(61,26,'Inicio de sesion ','2021-01-04 09:48:32','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(62,26,'Cierre de sesión','2021-01-04 21:23:58','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(63,26,'Inicio de sesion ','2021-01-05 17:07:46','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(64,26,'Cierre de sesión','2021-01-05 18:40:07','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(65,26,'Inicio de sesion ','2021-01-05 18:41:37','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(66,26,'Cierre de sesión','2021-01-05 18:44:03','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(67,26,'Inicio de sesion ','2021-01-05 18:44:42','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(68,26,'Cierre de sesión','2021-01-05 18:57:18','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(69,26,'Inicio de sesion ','2021-01-05 19:38:08','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(70,26,'Cierre de sesión','2021-01-06 10:06:32','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(71,26,'Inicio de sesion ','2021-01-06 15:30:08','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(72,26,'Cierre de sesión','2021-01-06 15:59:05','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(73,26,'Inicio de sesion ','2021-01-06 16:08:56','127.0.0.1',NULL),(74,26,'Cierre de sesión','2021-01-06 16:33:53','127.0.0.1',NULL),(75,26,'Inicio de sesion ','2021-01-06 16:35:01','127.0.0.1',NULL),(76,26,'Inicio de sesion ','2021-01-06 16:44:22','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(77,26,'Cierre de sesión','2021-01-06 16:44:29','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(78,26,'Cierre de sesión','2021-01-06 23:28:09','127.0.0.1',NULL),(79,26,'Inicio de sesion ','2021-01-07 22:03:47','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(80,26,'Cierre de sesión','2021-01-08 17:53:35','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(81,26,'Inicio de sesion ','2021-01-08 19:15:44','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(82,26,'Cierre de sesión','2021-01-12 00:20:06','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(83,26,'Inicio de sesion ','2021-01-13 20:07:25','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(84,26,'Inicio de sesion ','2021-01-18 22:56:43','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(85,26,'Cierre de sesión','2021-01-19 11:38:27','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(86,26,'Inicio de sesion ','2021-01-20 06:33:03','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(87,26,'Cierre de sesión','2021-01-20 06:44:46','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(88,26,'Inicio de sesion ','2021-01-20 06:46:49','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(89,26,'Cierre de sesión','2021-01-20 23:23:31','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(90,26,'Inicio de sesion ','2021-01-21 00:14:12','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(91,26,'Cierre de sesión','2021-01-21 02:21:05','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(92,26,'Inicio de sesion ','2021-01-21 09:27:01','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(93,26,'Cierre de sesión','2021-01-21 14:43:40','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(94,26,'Inicio de sesion ','2021-01-21 18:35:27','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(95,26,'Cierre de sesión','2021-01-21 18:35:31','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(96,26,'Inicio de sesion ','2021-01-21 18:47:04','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(97,26,'Cierre de sesión','2021-01-21 18:47:08','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(98,26,'Inicio de sesion ','2021-01-21 18:51:09','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(99,26,'Cierre de sesión','2021-01-21 18:51:16','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(100,30,'Inicio de sesion ','2021-01-21 20:05:47','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(101,30,'Cierre de sesión','2021-01-21 20:08:40','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(102,30,'Inicio de sesion ','2021-01-21 20:09:12','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(103,30,'Cierre de sesión','2021-01-21 20:24:05','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(104,26,'Inicio de sesion ','2021-01-21 20:24:24','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(105,26,'Cierre de sesión','2021-01-21 20:46:52','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(106,26,'Inicio de sesion ','2021-01-21 20:48:33','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(107,26,'Cierre de sesión','2021-01-21 21:07:36','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"'),(108,26,'Inicio de sesion ','2021-01-21 21:08:20','127.0.0.1','\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_online`
--

LOCK TABLES `ordenes_online` WRITE;
/*!40000 ALTER TABLE `ordenes_online` DISABLE KEYS */;
INSERT INTO `ordenes_online` VALUES (1,26,'Denis Vasquez','Tegucigalpa, Honduras','123333','lckskncksncnskc',318.00,18.00,'2021-01-05 20:15:08',0,37),(2,30,'pablo 1','None','12929938','Apartamento 3, edifico colonial ',243.80,13.80,'2021-01-21 20:16:42',0,43),(3,30,'pablo 1','None','12929938','Apartamento 3, edifico colonial ',243.80,13.80,'2021-01-21 20:16:43',0,43);
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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (3,'Refresco coca cola','2020-11-21 03:34:31',20.00,1,9,'1233',12.00,0,10,1,3,NULL,NULL,NULL),(4,'queso','2020-11-21 03:39:06',10.00,1,4,'2222',8.00,0,5,1,1,NULL,NULL,NULL),(5,'Te lipton','2020-11-21 03:41:41',18.00,1,9,'12234',10.00,0,10,1,3,NULL,NULL,NULL),(6,'Margarina','2020-11-21 04:03:31',15.00,1,1,'1222',10.00,0,12,2,4,NULL,NULL,NULL),(7,'pruebaa 2','2020-11-21 04:04:37',1222.00,0,8,'1222232',0.00,0,10,0,2,NULL,NULL,NULL),(8,'Producto3','2020-12-04 19:26:03',2000.00,0,1,'P3',0.00,0,10,1,1,NULL,NULL,NULL),(9,'Caja de carton','2020-12-09 20:40:06',30.00,0,1,'HT45',25.00,0,10,1,5,NULL,NULL,NULL),(10,'Caja de carton armable','2020-12-09 21:22:59',30.00,1,1,'ht45',23.00,0,10,1,5,'paquete de 3 cajas de carton armables, dimensiones 4x6x5',NULL,NULL),(11,'prueba 23','2020-12-10 15:07:56',12.34,1,1,'GEER3423',3.45,0,6,1,1,'prueba de producto',NULL,NULL),(12,'producto23||','2020-12-10 15:21:30',2322.00,1,1,'ewkk12',0.00,0,10,1,1,'blha vlvnandkqw kjkjskq',NULL,NULL),(17,'pruenaaaa','2020-12-10 22:52:16',20.00,1,7,'12122121',0.00,0,0,1,6,'',NULL,NULL),(18,'prueba sin imagen ','2020-12-10 23:18:01',1000.00,0,7,'1',0.00,0,0,1,6,'prueba  sin imagen',NULL,NULL),(19,'prueba con imagen ','2020-12-10 23:20:16',2000.00,1,7,'122222',0.00,0,1,1,6,'ldkldklakldalda',NULL,NULL),(20,'prueba 2 sin imagen ','2020-12-10 23:22:26',200.00,1,7,'9009203',0.00,0,0,1,6,'',NULL,NULL),(21,'prueba 2 con imagen ','2020-12-10 23:23:07',2000.00,0,10,'099009',0.00,0,10,1,5,'prueba de actualización de productos','bbaa302e-40df-11eb-bf02-94659c30abd3.jpg',NULL),(22,'sin imagen ','2020-12-10 23:31:37',2000.00,1,7,'11111111',0.00,0,0,1,6,'',NULL,NULL),(23,'con imagen ','2020-12-10 23:32:03',2000000.00,1,7,'3390200199828',0.00,0,0,1,6,'',NULL,NULL),(24,'prueba desde imagen','2020-12-17 21:45:15',2.30,1,NULL,'th56',0.00,0,9,NULL,NULL,'holla',NULL,NULL),(25,'nuevo producto probando ','2020-12-17 22:03:33',23.56,1,7,'90',20.09,0,10,1,6,'nuevo producto probando  descripcion','ff213bb3-40e5-11eb-9b8d-94659c30abd3.jpg',NULL),(26,'nuevo producto probando 2','2020-12-17 22:08:34',160.78,1,7,'91',0.00,0,20,0,6,'probando producto 2',NULL,NULL),(27,'probando producto 3 ','2020-12-17 22:32:21',102.20,1,NULL,'9',87.30,0,134,1,NULL,'prueba sin categoria y sin unidad',NULL,NULL),(28,'probando producto 4','2020-12-17 22:37:06',23.34,1,NULL,'94',23.20,0,10,1,NULL,'actualizado',NULL,NULL),(29,'probando nuevo 23232323','2020-12-17 22:44:36',12.00,1,1,'93',0.00,0,10,1,1,'malo ',NULL,NULL),(30,'prueba 123333','2020-12-19 17:26:09',2300.00,1,NULL,'673',0.00,0,10,1,NULL,'pruebaaa',NULL,NULL),(31,'Monitor','2020-12-19 22:41:14',12000.00,1,2,'547',10000.00,0,10,1,6,'Monitor HD con tecnologia oled','97b0583f-427d-11eb-a8d3-94659c30abd3.png',NULL),(32,'ROBOT','2020-12-19 23:51:21',300.00,1,11,'RB45',400.00,0,5,1,6,'Robot de juguete','63199d80-4287-11eb-b1d5-94659c30abd3.png',NULL),(33,'otrioiooeiieie','2020-12-27 17:39:11',10.00,1,NULL,'555',2.00,0,20,1,NULL,'',NULL,NULL),(34,'otrooo producto rueba ','2020-12-27 17:43:44',39.00,1,2,'lo90',20.00,0,11,1,2,'otjehjsbkjfjs',NULL,NULL),(35,'prueba1222','2020-12-27 17:46:02',1292.00,1,2,'P1222',900.00,0,5,1,2,'mchnksnkcnsc',NULL,NULL),(36,'Caja de leche ','2020-12-27 17:53:38',15.00,1,9,'L128',10.00,0,10,1,3,'Litro de leche en caja de larga duración','bd45b657-489e-11eb-a8d4-94659c30abd3.png','bd4331c8-489e-11eb-8943-94659c30abd3.png'),(37,'Alcohol etílico ','2021-01-08 20:06:24',40.00,1,12,'01',30.50,76,20,1,7,'Bote de alcohol etílico 70 grados de 1000 ml.','465ba4bf-521f-11eb-9b9a-94659c30abd3.jpg','45da75e6-521f-11eb-9227-94659c30abd3.png'),(38,'Gel antibacterial','2021-01-08 20:08:22',100.00,1,12,'02',80.00,796,20,1,7,'Bote de gel antibacterial, con 70% de alcohol. ','8cefc3b9-521f-11eb-aad3-94659c30abd3.jpg','8cef9d77-521f-11eb-a0f0-94659c30abd3.png'),(39,'Agua oxigenada','2021-01-08 20:10:21',50.00,1,12,'03',43.00,205,20,1,7,'Bote de agua oxigenada, presentación de 500 ml, marca H.E.B.','d3ada566-521f-11eb-ad3d-94659c30abd3.jpg','d3ad3026-521f-11eb-92c0-94659c30abd3.png'),(40,'Curas','2021-01-08 20:13:01',35.00,1,12,'04',27.50,10,15,1,8,'Caja de 50 curas o vendas medicas impermeables, marca CureBand.','33234e76-5220-11eb-a8a9-94659c30abd3.png','33230058-5220-11eb-9af2-94659c30abd3.png'),(41,'Esparadrapo ','2021-01-08 20:24:04',10.00,1,12,'05',6.30,500,20,1,9,'Esparadrapo medico marca M3, para uso medico y casero.','be441524-5221-11eb-8b59-94659c30abd3.jpg','be435f3b-5221-11eb-8a7d-94659c30abd3.png'),(42,'Algodón medico ','2021-01-08 20:25:59',40.00,1,12,'06',34.00,20,30,1,5,'Paquete de algodón para uso medico y casero, marca RBG.','02f933d3-5222-11eb-acbc-94659c30abd3.webp','02f8bf88-5222-11eb-97d3-94659c30abd3.png'),(43,'Mascarilla N95','2021-01-08 20:27:27',50.00,1,12,'07',38.30,40,60,1,9,'Mascarilla N95 unidad, marca 3M.','3793e9a5-5222-11eb-ba9b-94659c30abd3.png','37937556-5222-11eb-946a-94659c30abd3.png'),(44,'Papel higiénico','2021-01-08 20:31:49',130.00,1,13,'08',95.00,30,30,1,5,'Paquete de papel higiénico, 12 rollos doble hoja, marca premier.','d3467cbd-5222-11eb-b94f-94659c30abd3.webp','d346079a-5222-11eb-8e11-94659c30abd3.png'),(45,'Lysol ','2021-01-08 20:34:18',130.00,1,14,'09',96.00,29,30,1,7,'Bote de desinfectante en aerosol Lysol, presentacion de 400 ml.','2c7aea7d-5223-11eb-8906-94659c30abd3.jpg','2c7a7545-5223-11eb-8b84-94659c30abd3.png'),(46,'Mascarilla quirúrgica','2021-01-08 20:36:10',240.00,1,12,'10',120.00,0,30,1,5,'Caja de mascarillas quirúrgica, 20 unidades color azul.','6f063498-5223-11eb-8d7f-94659c30abd3.jpg','6f05c065-5223-11eb-99b4-94659c30abd3.png'),(47,'prueba 23445556','2021-01-20 08:59:53',23.00,1,1,'777',30.00,0,20,1,1,'prueba','26f38c03-5b30-11eb-9769-94659c30abd3.jpg','26ad6af4-5b30-11eb-8c08-94659c30abd3.png');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Plasticos estrella ','2021-01-21 10:46:39','23223490','plast@gmail.com',1,'Tegucigalpa 12345'),(2,'Variedades garcia','2021-01-21 12:03:03','34567888','garciasallud@yahoo.com',1,'Calle real, no. 3456, Comayagüela ');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respaldos`
--

LOCK TABLES `respaldos` WRITE;
/*!40000 ALTER TABLE `respaldos` DISABLE KEYS */;
INSERT INTO `respaldos` VALUES (1,'respaldo_sistema_20-01-2021_08_AM_37.sql',26,'2021-01-20 08:37:47'),(2,'respaldo_sistema_20-01-2021_09_04_AM.sql',26,'2021-01-21 00:14:59'),(3,'respaldo_sistema_21-01-2021_09_18_PM.sql',26,'2021-01-21 21:18:59');
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8 COMMENT='Almacenar compras temporal sin grabar.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temporal_compra`
--

LOCK TABLES `temporal_compra` WRITE;
/*!40000 ALTER TABLE `temporal_compra` DISABLE KEYS */;
INSERT INTO `temporal_compra` VALUES (2,'6331f8c1-8c66-4a94-9bd9-d2bf5eb3607e',3,'1233','Refresco coca cola',1,12.00,12.00),(11,'cd183780-e893-450e-bedd-463076ba6cbd',10,'ht45','Caja de carton armable',1,23.00,23.00),(12,'cd183780-e893-450e-bedd-463076ba6cbd',3,'1233','Refresco coca cola',1,12.00,12.00),(13,'178b6f60-0e01-4744-961c-15dc4228a216',10,'ht45','Caja de carton armable',1,23.00,23.00),(14,'97dd37a9-b49e-4a33-a283-073b38262ae4',10,'ht45','Caja de carton armable',1,23.00,23.00),(15,'1d875d21-7528-46ec-bf57-733079571736',10,'ht45','Caja de carton armable',12,23.00,276.00),(16,'6053df9e-c03a-4571-b57b-bdf6b47158c5',10,'ht45','Caja de carton armable',22,23.00,506.00),(17,'8e95525f-9982-474c-afa5-a54aebbe5a7b',3,'1233','Refresco coca cola',8,12.00,96.00),(22,'fd3e7f88-61f3-43f4-a5c8-009ff7f62813',3,'1233','Refresco coca cola',5,20.00,100.00),(23,'663ef1fa-7155-4750-bd2f-c13e409f3b54',10,'ht45','Caja de carton armable',20,30.00,600.00),(68,'60cc25ee-0210-465e-94cb-8cb61b47c011',3,'1233','Refresco coca cola',1,20.00,20.00),(69,'6a021c15-579d-47b2-8d51-804cd6d54362',3,'1233','Refresco coca cola',1,20.00,20.00),(76,'e00c040f-1aa0-499e-8363-1179e7e358c3',37,'01','Alcohol etílico ',60,30.50,1830.00),(77,'e2e4a1c5-6d1c-4d89-acea-ea28b45c58ac',37,'01','Alcohol etílico ',60,30.50,1830.00),(78,'e2e4a1c5-6d1c-4d89-acea-ea28b45c58ac',38,'02','Gel antibacterial',40,80.00,3200.00),(80,'ac57eda7-9428-4389-aa25-7e73c1457240',40,'04','Curas',4,35.00,140.00),(81,'bc05c4a3-9b6b-42d5-9cd6-cf0c1de83ca5',37,'01','Alcohol etílico ',4,40.00,160.00),(82,'17a3c7b4-ebd9-4670-b2ed-5d78ea800fc8',37,'01','Alcohol etílico ',1,30.50,30.50),(83,'443282da-2a68-4e96-abe7-00dcf18d03cb',37,'01','Alcohol etílico ',3,40.00,120.00),(90,'9e374c13-f102-4551-b0d9-3a9b0d7f3536',37,'01','Alcohol etílico ',4,30.50,122.00),(91,'9e374c13-f102-4551-b0d9-3a9b0d7f3536',39,'03','Agua oxigenada',5,43.00,215.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='manejo de medidas y unidades de los productos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades`
--

LOCK TABLES `unidades` WRITE;
/*!40000 ALTER TABLE `unidades` DISABLE KEYS */;
INSERT INTO `unidades` VALUES (1,'Libra','LB',1,'2020-11-20 19:28:53',NULL),(2,'Kilogramo','KG',1,'2020-11-20 21:25:47',NULL),(3,'Litro','LT',1,'2020-11-21 03:11:36',NULL),(4,'GRAMOS','G',1,'2020-11-21 14:30:55',NULL),(5,'Paquete','PQ',1,'2020-12-09 20:38:41',NULL),(6,'Sin unidad','SN',1,'2020-12-10 22:41:37',NULL),(7,'Bote','BT',1,'2021-01-08 20:04:03',NULL),(8,'Caja','CJ',1,'2021-01-08 20:11:02',NULL),(9,'Unidad','UN',1,'2021-01-08 20:22:58',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COMMENT='relacion de cajas con usuarios';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Alfa1','encargado','inactivo','2020-11-06 14:53:44','af1@gmail.com','1234',NULL,NULL,NULL,2,NULL),(3,'Maria Ramos','user','inactivo','2020-11-06 15:34:47','mramos@gmail.com','1234',NULL,NULL,NULL,NULL,NULL),(5,'Prueba Sabado','user','inactivo','2020-11-07 13:46:06','psat@unitec.edu','1234',NULL,NULL,NULL,NULL,NULL),(8,'Mario Alvarez','encargado','inactivo','2020-11-18 21:46:35','marz@unitec.edu','1234',NULL,NULL,NULL,NULL,NULL),(10,'Prueba login','Usuario','inactivo','2020-11-19 19:52:32','logon@gmail.com','$2b$12$gWzBECHPr6KRPE8IjFYX0.pNNWsJ/.XJJItjWigJcGkpmqoQGxFIG',NULL,NULL,NULL,NULL,NULL),(11,'prueba2 login','Usuario','activo','2020-11-19 20:02:04','log2@gmail.com','$2b$12$tzHwJJEHL1/YqVBKuHYI9OOcNBrMcgNDZ5ru2/sGoBDyJnzhtNJDe',NULL,NULL,NULL,NULL,NULL),(18,'prueba45','Usuario','activo','2020-11-19 22:41:52','prueba45@gmail.com','$2b$12$iC30EOtDuhj2X5SxpNdb0Opiu7wiQpBxw1cmmTzQ7uYkvcIuZu0vS',NULL,NULL,NULL,NULL,NULL),(20,'pruebalogin3','Usuario','inactivo','2020-11-19 22:47:20','pruebalog@gmail.com','$2b$12$N28Oqw2TxGvwRbnAjo8i1eX3UtbZc/lsYOFluds8w3yqJBf8xTDA6',NULL,NULL,NULL,NULL,NULL),(23,'prueba login','Usuario','activo','2020-11-19 23:38:48','pree@gmail.com','$2b$12$WNR0XtoLVixcUFaw.pSgZOhHmjw2.EWxlFzQdkq8Qk/GOV7FXe7Mi',NULL,NULL,NULL,NULL,NULL),(24,'prueba login','Usuario','activo','2020-11-19 23:44:55','asma@dww.com','$2b$12$x0ofK1jDRqzNwiBEpvyMF.nhxU.vjyNy8fKJL4BGVaheV0jS5gOwC',NULL,NULL,NULL,NULL,NULL),(25,'prueba 123','usuario','inactivo','2020-11-20 02:25:30','prueba@gmail.com','$2b$12$6bNChSc5YUdpJigrBThqBe221JFhkcF5Qcjs1dNxIhtTXfXe0ULL6',NULL,NULL,NULL,NULL,NULL),(26,'Denis Vasquez','admin','activo','2020-11-20 02:36:55','denisvsnew@gmail.com','$2b$12$bYenmtbJF5gOg2sal8kR7.0dJ7uZ4ynRQ1KijUzIqwXwMciWxURQ.','85246871','Tegucigalpa, Honduras','e39f16ce-3acc-11eb-8f59-94659c30abd3.png',2,'ImRlbmlzdnNuZXdAZ21haWwuY29tIg.YAogAg.xoT--1XWHLCS1kKOODmljD7rqAg'),(27,'Astón Umaña','usuario','activo','2020-11-20 17:33:05','astn@gmail.com','$2b$12$xaY3ts8qODDT.NO3X4TL0u7gzGmOQro13.wFB3nEtdf6UAaXXrhnq',NULL,NULL,NULL,NULL,NULL),(28,'ejemplo','usuario','activo','2020-11-21 14:29:02','ejemplo@algo.com','$2b$12$DLQEXVfUjTogmx3jTp9TKuuGeRCwPv0DqPW0j3/HyMDOBpWHaYUTi',NULL,NULL,NULL,NULL,NULL),(30,'pablo 1','usuario','activo','2020-12-15 11:15:49','pablo1@gmail.com','$2b$12$STA4R.VK5fKNgyxX4FMSEe2pYdTNaXHV0xA1NlV70d8ZdBooq97t.',NULL,NULL,'imagen-no-disponible.jpg',NULL,NULL),(31,'ZAP','usuario','activo','2021-01-06 23:31:09','foo-bar@example.com','$2b$12$aVR08Gcy.//gzDdhjV7B1uE1rE6GEYzqTEXA28xiAEpk2YMk0kQEO',NULL,NULL,NULL,NULL,NULL),(32,'Marco Padilla','usuario','activo','2021-01-21 19:09:14','hilib14056@1adir.com','$2b$12$KZ7DHnWcFU3iwWaESoYogOJzoWlVoL7CxhD6IDsxTGFofFbYLOZpC','34330293','Tegucigalpa','61fa50cf-5c50-11eb-8ba0-94659c30abd3.png',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (3,'2020-12-19 03:45:08',1640.00,26,NULL,0,1,'e7bf3000-00c8-4805-ac8f-543ad4dbd0ac',1,NULL,NULL),(4,'2020-12-19 09:03:31',2000.00,26,NULL,1,NULL,'d9861a0b-b960-42dc-86d3-d038b05d2566',1,NULL,NULL),(5,'2020-12-21 21:54:55',150.00,26,NULL,1,1,'0e7548f9-2474-415f-a80d-caa4f2701ffc',NULL,NULL,NULL),(6,'2020-12-22 00:01:46',469.94,26,NULL,1,1,'dca2bdda-4638-4824-bbe6-5996360faecb',NULL,NULL,NULL),(7,'2020-12-22 00:10:49',6000.00,26,NULL,1,1,'6abe93fe-e89b-4d13-8665-48e496e63c91',NULL,NULL,NULL),(8,'2020-12-22 00:13:50',600.00,26,NULL,1,1,'981ce74a-e0ab-49f3-95c7-b6f6eda1de81',NULL,NULL,NULL),(9,'2020-12-22 07:48:59',90.00,26,NULL,1,1,'e306403e-d63f-4e25-93d5-aa03afa30141',NULL,NULL,NULL),(10,'2020-12-22 08:01:49',90.00,26,2,1,1,'e6ffd501-5790-448a-ac85-45ba7390f47e',NULL,NULL,NULL),(11,'2020-12-22 10:49:13',60.00,26,3,1,1,'fbff7b83-eaed-416d-a83a-1df0f6cdff43',NULL,NULL,NULL),(12,'2020-12-22 10:55:52',60.00,26,1,1,1,'d377d48a-7ea3-4847-8cf7-31fffe5c9d16',NULL,NULL,NULL),(13,'2020-12-22 11:31:45',60.00,26,1,1,1,'3cc9df9f-c0a9-4aff-9f04-41136dbcbbf3',NULL,NULL,NULL),(14,'2020-12-23 12:01:49',30.00,26,1,1,1,'d5c9bf42-5fc6-4356-b050-c54d1e3b5742',NULL,NULL,NULL),(15,'2020-12-24 01:43:17',30.00,26,3,1,1,'589e2532-d26e-49d4-872d-53b455b81841',NULL,NULL,NULL),(16,'2020-12-24 02:21:40',25320.00,26,2,1,1,'05d6e8fe-61e9-4492-b24d-e5a71287dc06',NULL,NULL,NULL),(17,'2020-12-24 02:30:23',1320.00,26,7,1,1,'0114de93-dabf-4d47-b02a-94460809b317',NULL,NULL,NULL),(18,'2020-12-24 02:32:02',1320.00,26,7,1,1,'6ddd1115-6808-4a21-aa3b-3e0c2d3f52b3',NULL,NULL,NULL),(19,'2020-12-24 02:37:30',30.00,26,1,0,1,'7bdc4ee2-28a8-4644-af80-f1efef301d2a',NULL,NULL,NULL),(20,'2020-12-26 16:00:00',80.00,26,7,1,1,'26e146a8-8a4a-4ee9-ae8d-9bcdb0f2bb7e',NULL,NULL,NULL),(21,'2020-12-27 02:06:28',800.00,26,2,1,1,'2f4d06e5-19fc-4ba1-8d42-b704d620c9a8',NULL,NULL,NULL),(23,'2020-12-29 13:53:16',20.00,26,2,1,1,'3d4d0951-88ce-4dc8-97e4-b6a7bb850fb0',NULL,NULL,NULL),(24,'2020-12-30 01:21:30',620.00,26,2,1,1,'1',2,NULL,NULL),(25,'2020-12-30 01:23:46',600.00,26,2,1,1,'2',2,NULL,NULL),(26,'2021-01-04 01:20:25',100.00,26,2,1,1,'3',2,NULL,NULL),(27,'2021-01-04 02:42:23',120.00,26,7,1,1,'4',2,4,NULL),(28,'2021-01-04 09:58:36',20.00,26,7,1,1,'5',2,4,NULL),(29,'2021-01-04 10:41:21',20.00,26,7,1,1,'6',2,5,NULL),(30,'2021-01-04 10:41:47',90.00,26,7,1,1,'7',2,5,NULL),(31,'2021-01-04 10:42:30',70.68,26,7,1,1,'8',2,5,NULL),(34,'2021-01-05 19:42:43',318.00,26,15,1,1,'63ea318e-5062-47d2-8469-2c4397aae33c',NULL,NULL,2),(35,'2021-01-05 19:45:19',318.00,26,15,1,1,'4661c96b-218f-4ab8-bd73-5d24ed63043f',NULL,NULL,2),(36,'2021-01-05 19:53:42',318.00,26,15,1,1,'21a440c2-2a8d-4656-8d5b-e53779d9b8cf',NULL,NULL,2),(37,'2021-01-05 20:15:08',318.00,26,15,1,1,'a2d61d81-1343-45d9-85c7-6406e2ce4c8f',NULL,NULL,2),(38,'2021-01-06 16:29:21',90.00,26,2,0,1,'9',2,6,NULL),(39,'2021-01-06 16:29:22',90.00,26,2,1,1,'10',2,6,NULL),(40,'2021-01-08 21:21:35',120.00,26,7,1,1,'11',2,6,NULL),(41,'2021-01-08 23:11:30',600000.00,26,7,1,1,'12',2,6,NULL),(42,'2021-01-20 08:55:49',40.00,26,7,1,1,'13',2,6,NULL),(43,'2021-01-21 20:16:40',243.80,30,15,1,1,'4dab7e55-ffe0-419d-be77-6bb77beac118',NULL,NULL,2),(44,'2021-01-21 20:58:52',250.00,26,7,0,1,'14',2,7,NULL),(45,'2021-01-21 21:03:06',250.00,26,7,0,1,'15',2,7,NULL),(46,'2021-01-21 21:05:33',300.00,26,7,1,1,'16',2,7,NULL);
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

-- Dump completed on 2021-01-21 21:19:04
