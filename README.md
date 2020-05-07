# Detector de mascarillas en el rostro

<p align="center">
<img width="600" src=astronomia.png>
</p>

En esta sencilla prueba de concepto creamos un detector de máscara facial que nos proteja del COVID-19 con OpenCV, Keras/TensorFlow y Deep Learning.

## Fases
Para entrenar un detector de máscara facial personalizado, necesitamos dividir nuestro proyecto en dos fases distintas, cada una con sus propios subpasos respectivos (como se muestra en la Figura 1 anterior):

* **Entrenamiento**: aquí nos enfocaremos en cargar nuestro conjunto de datos de detección de máscara facial desde el disco, entrenar un modelo (usando Keras / TensorFlow) en este conjunto de datos y luego serializar el detector de máscara facial en local;
* **Despliegue**: Una vez que el detector de máscara facial está entrenado, podemos pasar a cargar el detector de máscara, realizar la detección de la cara y luego clasificar cada cara como *Mask* o *No Mask*.

## Instalando el entorno

Se puede hacer uso de Anaconda para la creación de un entorno virtual.

```bash 
$ conda create --name <env> --file environment.yml
```

## Dataset
El conjunto de datos usados se ha obtenido del [siguiente repositorio](https://github.com/prajnasb/observations) y se ha completado con algunas imágenes más de individuos de razas más dispares para garantizar un modelo más robusto.

En total, el conjunto de datos consta de **1.442 imágenes** que pertenecen a dos clases:

* **Con máscara**: 723 imágenes
* **Sin máscara**: 719 imágenes

<p align="center">
<img width="600" src=sprite.jpg>
</p>

Este método es en realidad mucho más fácil de lo que parece una vez que aplica puntos de referencia faciales al problema.

Los puntos de referencia faciales nos permiten inferir automáticamente la ubicación de las estructuras faciales, que incluyen:

* Ojos
* Cejas
* Nariz
* Boca
* Contorno del rostro

Para quedarnos con la **Region of Interest** (ROI) que enmarca el rostro. Entendemos que incluir la máscara en las imágenes y tapar ciertos landmarks ayudará al modelo a discrtizar las muestras satisfactoriamente.

Sobre el dataset disponible se hace data augmentation durante el entrenamiento:
* **Rotación aleatoria** de cada imagen de hasta `20 grados`;
* **Desplazamiento en altura y anchura** de hasta el `20%` de la dimensión de la imagen;
* **Horizontal flipping**;
* **zoom_range** de 0.15;
* **shear_range** de 0.15.

## Entrenando el modelo

Se usa **Keras** y **TensorFlow** para entrenar a un clasificador para detectar automáticamente si una persona usa una máscara o no.

Para llevar a cabo esta tarea, ajustaremos la arquitectura **MobileNet V2**, una arquitectura altamente eficiente que se puede aplicar a dispositivos integrados con capacidad computacional limitada (por ejemplo, Raspberry Pi, Google Coral, NVIDIA Jetson Nano, etc.).

Ejecutando el siguiente comando:
```bash
$ python train_mask_detector.py --dataset dataset
```

Se lanza un entrenamiento que terminará cuando la condición de `EarlyStopping` implementada se cumpla. Lo que estamos haciendo es un *fine-tuning* de **MobileNetv2** para ahorrar tiempo y garantizar una buena predicción.

Se obtienen dos checkpoints tras el entrenamiento: `mask_detector_model.h5` y `mask_detector.model`.  
### Logueo del entrenamiento
El resultado del entrenamiento actual se puede consultar en TensorBoard.

```bash
$ tensorboard --logdir logs
```
Una vez se haya habilitado el servicio de monitorización, podemos analizar las curvas de la función de pérdida y precisión tanto sobre el training como el test dataset en local a través de:

```bash
http://localhost:6006
```
Actualmente, la precisión sobre el test dataset estaba alrededor del `98%`, lo suficientemente alto como para considerar que el modelo de clasificación es de buena calidad.

## Detectando muestras tras el entrenamiento

### Imágenes
Ahora que nuestro detector de mascarillas está entrenado, podemos:

* Cargar una imagen de entrada desde el disco
* Detectar rostros en la imagen.
* Aplique nuestro detector de mascarilla para clasificar la cara como `con máscara` o `sin máscara`.

Para ello símplemente tenemos que ejecutar:
```bash
$ python detect_mask_image.py --image <route-to-image>
```
Esto nos devolverá la imagen con los rostros identificados y con una etiqueta de si lleva máscara o no.

### Vídeo
Nuestro detector de mascarillas COVID-19 también puede funcionar en tiempo real.

Símplemente ejecutamos en terminal:
```bash
$ python detect_mask_video.py
```
Para poder servir en vídeo desde la webcam de nuestro dispositivo las predicciones de nuestro modelo.
<video width="500" controls>
  <source src="face-mask-detector.mp4" type="video/mp4">
</video>

## TODOs
1. Se puede mejorar la calidad del dataset a usar.
2. Hay que tener en cuenta que para clasificar si una persona usa o no una máscara, primero debemos realizar la detección del rostro: si no se encuentra una cara, entonces el detector de máscara no se puede aplicar.

La razón por la que no podemos detectar la cara en primer plano es porque:

* Está demasiado oscurecido por la máscara.
* El rostro está demasiado ocluido por la máscara.

Se debe pensar en cómo mejorar esto. Ahora bien, el impacto de este caso es mínimo en nuestro modelo.