-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-04-2025 a las 17:59:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `smartgrow`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `idClientes` int(11) NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Telefono` varchar(20) DEFAULT NULL,
  `Tipo_plan` enum('Basico',' Estandar','Premium') DEFAULT NULL,
  `Contraseña` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clima_local`
--

CREATE TABLE `clima_local` (
  `idClima_local` int(11) NOT NULL,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Temperatura` decimal(5,2) DEFAULT NULL,
  `Humedad` decimal(5,2) DEFAULT NULL,
  `Lluvia` decimal(5,2) DEFAULT NULL,
  `Luz` int(11) DEFAULT NULL,
  `Viento` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultas`
--

CREATE TABLE `consultas` (
  `idConsultas` int(11) NOT NULL,
  `Fecha_consulta` date DEFAULT NULL,
  `Hora_consulta` time DEFAULT NULL,
  `Descripcion_problema` text DEFAULT NULL,
  `Respuesta` text DEFAULT NULL,
  `Tiempo_respuesta` int(11) DEFAULT NULL,
  `Expedientes_idExpedientes` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_api`
--

CREATE TABLE `datos_api` (
  `idDatos_API` int(11) NOT NULL,
  `Expedientes_id` int(11) NOT NULL,
  `Datos_clima_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_clima`
--

CREATE TABLE `datos_clima` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Temperatura` decimal(5,2) DEFAULT NULL,
  `Humedad` decimal(5,2) DEFAULT NULL,
  `Lluvia` decimal(5,2) DEFAULT NULL,
  `Luz` int(11) DEFAULT NULL,
  `Viento` decimal(5,2) DEFAULT NULL,
  `torre` int(11) DEFAULT NULL,
  PRIMARY KEY (`idDatos_clima`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estacion`
--

CREATE TABLE `estacion` (
  `idEstacion` int(11) NOT NULL,
  `Ubicacion_geografica` point DEFAULT NULL,
  `Altitud` decimal(6,2) DEFAULT NULL,
  `Estado` enum('Activa','Inactiva','Mantenimiento') DEFAULT NULL,
  `Expedientes_id` int(11) NOT NULL,
  `Clima_local_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `expedientes`
--

CREATE TABLE `expedientes` (
  `idExpedientes` int(11) NOT NULL,
  `Tipo_cultivo` varchar(100) DEFAULT NULL,
  `Ubicacion` varchar(255) DEFAULT NULL,
  `Tamaño` decimal(10,2) DEFAULT NULL,
  `Problematica` text DEFAULT NULL,
  `Nombre_empresa` varchar(100) DEFAULT NULL,
  `Clientes_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idClientes`);

--
-- Indices de la tabla `clima_local`
--
ALTER TABLE `clima_local`
  ADD PRIMARY KEY (`idClima_local`);

--
-- Indices de la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD PRIMARY KEY (`idConsultas`),
  ADD KEY `fk_Consultas_Expedientes1_idx` (`Expedientes_idExpedientes`);

--
-- Indices de la tabla `datos_api`
--
ALTER TABLE `datos_api`
  ADD PRIMARY KEY (`idDatos_API`),
  ADD KEY `fk_Datos_API_Expedientes_idx` (`Expedientes_id`),
  ADD KEY `fk_Datos_API_Datos_clima1_idx` (`Datos_clima_id`);

--
-- Indices de la tabla `datos_clima`
--
ALTER TABLE `datos_clima`
  ADD PRIMARY KEY (`idDatos_clima`);

--
-- Indices de la tabla `estacion`
--
ALTER TABLE `estacion`
  ADD PRIMARY KEY (`idEstacion`),
  ADD KEY `fk_Estacion_Expedientes1_idx` (`Expedientes_id`),
  ADD KEY `fk_Estacion_Clima_local1_idx` (`Clima_local_id`);

--
-- Indices de la tabla `expedientes`
--
ALTER TABLE `expedientes`
  ADD PRIMARY KEY (`idExpedientes`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD CONSTRAINT `fk_Consultas_Expedientes1` FOREIGN KEY (`Expedientes_idExpedientes`) REFERENCES `expedientes` (`idExpedientes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `datos_api`
--
ALTER TABLE `datos_api`
  ADD CONSTRAINT `fk_Datos_API_Datos_clima1` FOREIGN KEY (`Datos_clima_id`) REFERENCES `datos_clima` (`idDatos_clima`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Datos_API_Expedientes` FOREIGN KEY (`Expedientes_id`) REFERENCES `expedientes` (`idExpedientes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `estacion`
--
ALTER TABLE `estacion`
  ADD CONSTRAINT `fk_Estacion_Clima_local1` FOREIGN KEY (`Clima_local_id`) REFERENCES `clima_local` (`idClima_local`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Estacion_Expedientes1` FOREIGN KEY (`Expedientes_id`) REFERENCES `expedientes` (`idExpedientes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `expedientes`
--
ALTER TABLE `expedientes`
  ADD CONSTRAINT `expedientes_ibfk_1` FOREIGN KEY (`idExpedientes`) REFERENCES `clientes` (`idClientes`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;