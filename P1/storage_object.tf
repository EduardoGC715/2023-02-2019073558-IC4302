resource "oci_objectstorage_bucket" "bucket" {
    compartment_id = var.compartment_id
    name = var.bucket_name
    namespace = data.oci_objectstorage_namespace.namespace.namespace
}
