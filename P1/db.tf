resource "oci_database_autonomous_database" "autonomous_database" {
  compartment_id = var.compartment_id
  db_name = var.db_name
  admin_password = var.db_password
  is_free_tier = true
  is_mtls_connection_required = false
#  tls_authentication = "SERVER"
  whitelisted_ips = [oci_core_instance.vm01.public_ip]
}

resource "oci_nosql_table" "logs_table" {
    compartment_id = var.compartment_id
    ddl_statement = "CREATE TABLE if not exists ${var.db_name}_logs (logId INTEGER, title STRING, bagInfo JSON, PRIMARY KEY (logId))"
    name = "${var.db_name}_logs"
    table_limits {
	max_storage_in_gbs = 1
	max_read_units = 1
	max_write_units = 1
    }
}
    


