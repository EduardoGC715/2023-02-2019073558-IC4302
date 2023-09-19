variable "compartment_id" {
  description = "OCID from your tenancy page"
  type        = string
}
variable "region" {
  description = "region where you have OCI tenancy"
  type        = string
}
variable "public_subnet_cidr_block" {
  description = "Public subnet CIDR block"
  type        = string
}

variable "cidr_block" {
  description = "VCN CIDR block"
  type        = string
}

variable "bucket_name" {
  description = "Name of Object Storage Bucket"
  type        = string
}

variable "db_name" {
  description = "Name of the database to create"
  type        = string
  default     = "ic4302"
}

variable "db_password" {
  description = "Password of the database"
  type        = string
  default     = "thisiswrongNereo08"
}




variable "os_image_id" {
  default = "ocid1.image.oc1.us-chicago-1.aaaaaaaaatkvmql7wfdyx2tzkcrbq6zxmtu2vfn4impe256wrh4cdwlg6lhq"
}


