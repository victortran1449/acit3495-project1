# acit3495-project1

#### create cluster on eks
- eksctl create cluster --name=project2 --region=us-west-2
- create access entry for root user (AmazonEKSClusterAdminPolicy)
- add AmazonElasticFileSystemFullAccess policy to NodeInstanceRole for cluster

#### create resources
- kubectl apply -f kubernetes/config-maps
- kubectl apply -f kubernetes/secrets
- kubectl apply -f kubernetes/persistent-volumes
- kubectl apply -f kubernetes/services
- kubectl apply -f kubernetes/deployments
- kubectl apply -f kubernetes/enterdata-app-hpa.yaml

#### create efs
- create efs
- edit volume mounts to include ClusterSharedNodeSecurityGroup from cluster
- change storage class to match efs id that was created (kubernetes/persistent-volumes/storage-class.yaml)

#### install aws-efs-csi driver
- helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver/
- helm repo update
- helm install aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver --namespace kube-system

#### auto scaling demo
- watch 'kubectl get po;kubectl top pods
- hey -z 4m -c 25 <ENTER_DATA_LOADBALANCER_IP>

#### delete cluster and efs
- eksctl delete cluster project2