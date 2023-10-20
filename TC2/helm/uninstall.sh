
# Uninstall backups
helm uninstall backups || true

# Uninstall databases
helm uninstall databases || true 

# Uninstall bootstrap
helm uninstall bootstrap || true



# Remove downloaded chart dependencies
#rm -rf bootstrap/charts
#rm -rf databases/charts
#rm -rf backups/charts

# Remove cached chart repositories
#helm repo remove elastic
#helm repo remove bitnami
#helm repo remove couchdb
#helm repo remove neo4j