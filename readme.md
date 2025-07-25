# Enhancing Carpet Dsign with GAN(Generative Adversarial Networks)

## Outputs

| User Uploads | GAN Enhanced Designs |
|--------------|----------------------|
| [![User Upload 1](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/user_uploads/1708195319.jpg)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/user_uploads/1708195319.jpg) | [![GAN Design 1](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/final_design.png)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/final_design.png) |
| [![User Upload 2](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/user_uploads/1708224295.jpg)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/user_uploads/1708224295.jpg) | [![GAN Design 2](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708195332.jpg)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708195332.jpg) |
|              | [![GAN Design 3](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708189061.jpg)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708189061.jpg) |
|              | [![GAN Design 4](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708189054.jpg)](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/media/generated_files/stylized_1708189054.jpg) |


### See more outputs
To see more generated files by our system visit [Here](https://github.com/99-NinetyNine/GAN_rug_design/tree/master/media/generated_files) .
### Project Report
[Available Here](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/carpetDesignWithGAN.pdf)

### Project Report Slide
[Available Here](https://github.com/99-NinetyNine/GAN_rug_design/blob/master/REPORT_on_CARPET_DESIGN_using_GAN.pdf)


## Run Project 
### Clone Project
```bash
   git clone https://github.com/99-NinetyNine/GAN_rug_design.git
```
### Create a Virtual Environment
   ```bash
      # On Windows
      python -m venv env

      # On Linux/Mac
      python3 -m venv env
   ```
### Activate Virtual Environment
   ``` bash
      # On Windows
      .\env\Scripts\activate

      # On Linux/Mac
      source env/bin/activate
   ```
### Install Requirements
   ```bash

      pip install -r requirements.txt
```
### Run 
   ```bash
      uvicorn server:app --reload
   ```



## Link to the frontend application is provided here:
[Github](https://github.com/surajniroula789/rug-Frontend/)
