1. Get two two elastic IPs allocated -> Give these names for you group (1,2,3)
2. Create VPC with public/private subnets - > second option on VPC Wizard
  - Assign on the Elastic IPs to your VPC when it asks
3. Create a NAT gateway with your VPC’s public subnet and the 2nd elastic IP you created
4. This probably happens automatically - in route tables, public subnet should be assigned to the route table that points to your Internet Gateway (IGW)
5. In route tables, private subnet should be assigned the route table that points to your NAT gateway
  - If needed you may need to edit subnet associations for the route tables to achieve this 
7. Create Subnet Groups in the Redshift console against yor VPC -> hover over Config, choose Subnet Groups
  - Give it a name and a description
  - After choosing your VPC choose `Add all of the subnets for VPC`
8. Create Cluster with default settings on free-tier but change VPC target in `Network Configuration`
9. `yarn` install and `sls package` for to create a Python lambda zip
10. Create lambda and put in private subnet
11. Upload zip to lambda - `serverless` outputs this to `./.serverless/` in your project folder - it's the longer named `zip`
12. In the Lambda AWS Console for your lambda add the following environment variables
  - DB_HOST (private IP of Redshift Cluster -> Properties -> Connection Details -> View all connectioin details)
  - DB_USER (user that was set up on Cluster creation -> Redshift will default `awsuser`)
  - DB_PORT (5439)
  - DB_CLUSTER (ClusterID - usually same as name - Cluster -> Properties)
  - DB_NAME (`dev` is the default that Redshift creates, if you created another you may want to use that)
13. Add policy to lambda execution role with the following permissions:
  - Edit `Basic Settings` in Lambda console for your Lambda
  - Click view `[random lambda role name]` policy
  - Create a policy with the following permissions
    - Redshift - DescribeClusters, GetClusterCredentials
      - Check `any in this account` for Resources for `dbuser` and `dbname`
    - Redshift Data API - ExecuteStatement
  - Add policy to Lambda role
14. In lambda `Basic Settings` edit `Lambda Handler` to `handler.start` = `module.function`
16. Running the lambda successfully should add a new table to the Cluster called `test_table` viewable under `public` schema
17. In apply the learning from this process the `psycopg2` module in this project must be downloaded directly from - https://github.com/jkehler/awslambda-psycopg2. Follow the instructions on that repo