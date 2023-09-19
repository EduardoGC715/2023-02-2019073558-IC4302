# https://github.com/garutilorenzo/oracle-cloud-terraform-examples/blob/master/simple-instance/files/oci-ubuntu-install.sh
# https://github.com/garutilorenzo/oracle-cloud-terraform-examples/blob/master/simple-instance/compute.tf

data "cloudinit_config" "vm01" {
  gzip          = true
  base64_encode = true

  part {
    content_type = "text/x-shellscript"
    content      = templatefile("${path.module}/templates/vm01.sh", {})
  }
}

resource "oci_core_instance" "vm01" {
    availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
    compartment_id = var.compartment_id
    display_name = "vm01"
    shape = "VM.Standard.A1.Flex"
    shape_config {
        memory_in_gbs = "6"
        ocpus         = "1"
    }
    source_details {
        source_type = "image"
        source_id = var.os_image_id
    }
    create_vnic_details {
        subnet_id = oci_core_subnet.public.id
        assign_public_ip = true
    }
    freeform_tags = {
        "Name" = "vm01"
    }
    metadata = {
        ssh_authorized_keys = file("ssh/db2.pub")
        user_data           = data.cloudinit_config.vm01.rendered
    }
    preserve_boot_volume = false

}

output "vm01_connect" {
  value = "ssh -i ssh/db2 ubuntu@${oci_core_instance.vm01.public_ip}"
}
