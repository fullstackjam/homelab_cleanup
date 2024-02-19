Gitea
kubectl get secret gitea.admin -n global-secrets -o jsonpath='{.data.password}' | base64 --decode && echo

ArgoCD
./scripts/argocd-admin-password

Grafana
kubectl get secret dex.grafana -n global-secrets -o jsonpath='{.data.client_secret}' | base64 --decode && echo




argocd login argocd.eaglepass.io --grpc-web --no-verify
argocd proj windows add default -k deny --schedule "* * * * *" --duration 24h --namespaces * --manual-sync

argocd app set gitea --repo https://github.com/brimdor/homelab
argocd app sync gitea

argocd proj windows delete default


kubectl scale deployment sonarr-deployment --replicas=0 -n sonarr


backup
locate backup -> Operation -> Restore Latest Backup
Use Previous Name -> Click OK
Volume -> search by PVC Name -> input name -> Click Go
k3s kubectl scale deployment <name of deployment> --replicas=0 -n <namespace>
Hover over action menu to the right of the restored Backup -> Create PV/PVC -> Click OK
k3s kubectl scale deployment <name of deployment> --replicas=1 -n <namespace>


Restore Backup
Login to ArgoCD
Set Window to stop Sync
Do a more recent backup of whatever you need to expand. You will have to delete the current PVC in order to establish an expanded one.
Spin down to 0 replicas
Adjust Helm Chart or Yaml deployment to claim the new amount.
After backup, delete current pvc
Restore backup
Expand backup to designated size matching the yaml.
Create PV/PVC
Spin up replicas for application
All done




k3s kubectl get pods --all-namespaces | grep grafana
 
k3s kubectl -n grafana exec -it pods/grafana-*-* -- /bin/sh
 
grafana-cli admin reset-admin-password admin