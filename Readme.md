1. Get two two elastic IPs allocated
2. Create VPC with public/private subnets - > second option on VPC Wizard
  - Assign on the Elastic IPs to your VPC when it asks
3. Create a NAT gateway with your VPC’s public subnet and the 2nd elastic IP you created
4. In route tables, public subnet should be assigned to the route table that points to your Internet Gateway (IGW)
5. In route tables, private subnet should be assigned the route table that points to your NAT gateway
  - If needed you may need to edit subnet associations for the route tables to achieve this 
7. Create Subnet Groups against your VPC in Redshift for your Cluster -> hover over Config, choose Subnet Groups
8. Create Cluster with default settings on free-tier but change VPC target in `Network Configuration`
9. `yarn` install and `sls package` for to create a Python lambda zip
10. Create lambda and put in private subnet
11. Upload zip to lambda - `serverless` outputs this to `./.serverless/` in your project folder - it's the longer named `zip`
12. Add env variables
  - DB_HOST (private IP of Redshit Cluster)
  - DB_USER (user that was set up on Cluster creation)
  - DB_PORT (5439)
  - DB_CLUSTER (ClusterID - usually same as name - Cluster -> Properties)
13. Add policy to lambda execution role with the following permissions:
  - Redshift - DescribeClusters, GetClusterCredentials
  - Redshift Data API - ExecuteStatement
16. Running the lambda successfully should add a new table to the Cluster called `test_table` viewable under `public` schema