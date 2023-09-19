# Infraestructura en Azure Cloud

## Requerimientos:

* [Oracle CLI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm)
* [Terraform](https://developer.hashicorp.com/terraform/downloads)
* Tener una cuenta de Oracle Cloud, la invitación fue enviada a inicios de semestre.

## Creación de la infraestructura

* Abrir una terminal PowerShell/Linux
* Iniciar sesión en Oracle Cloud, para lograr esto se debe ejecutar el siguiente comando:

```bash
oci setup config
```
* Ingresar a la carpeta **P1* y editar el archivo **conf\group.tfvars**, establecer un nombre sin caracteres especiales, espacios o mayusculas:

```hcl
bucket_name = "{nombre del grupo sin espacios o caracteres especiales}"
region = "{Region seleccionada cuando se creo la cuenta de Oracle Cloud}"
compartment_id = "{tenant id, luego de iniciar sesión dar clic en Profile > Tenancy y copiar el OCID}"
os_image_id = "{OCID de la image del sistema operativo a usar}"
```

* Crear la infraestructura

```bash
terraform init
terraform apply --var-file=config/group.tfvars
```

* Si ocupan cambiar algo en los archivos de infraestructura ejecutan:

```bash
terraform init
terraform apply --var-file=config/group.tfvars
```

* Si ocupan borrar solo ejecutan:
```bash
terraform init
terraform destroy --var-file=config/group.tfvars
```

**IMPORTANTE**: Guarden en sus repositorios todos los archivos generados menos las carpetas .terraform y .terraform.lock.hcl, siempre deben guardar **terraform.tfstate** y **terraform.tfstate.backup**