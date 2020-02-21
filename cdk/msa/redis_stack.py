from aws_cdk import (
    aws_elasticache as redis,
    aws_ec2 as ec2,
    core
) 

class RedisStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
        vpc = ec2.Vpc.from_vpc_attributes(self, 'vpc',vpc_id=vpc.vpc_id,availability_zones=['us-east-1a','us-east-1b'])

        subnets = [ ps.subnet_id for ps in vpc.private_subnets]

        sg = ec2.SecurityGroup(self,'rdsSG',
            vpc=vpc,
            security_group_name='RedisSG',
            description="SG for Redis Cache",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.all_tcp(),description="SSH Access")

        subnet_group = redis.CfnSubnetGroup(self,'redis-sg',
            subnet_ids=subnets,
            description='subnet group for redis'
        )

        redis_cluster = redis.CfnCacheCluster(self, 'redis',
                cache_node_type='cache.t2.small',
                engine='redis',
                num_cache_nodes=1,
                cluster_name='msa-redis-dev',
                cache_subnet_group_name=subnet_group.ref,
                vpc_security_group_ids=[sg.security_group_id],
                auto_minor_version_upgrade=True

        )
        redis_cluster.add_depends_on(subnet_group)
        
        core.CfnOutput(self,'redissg',
            value=sg.security_group_id,
            export_name='redis-sg-export'
        )

        #redis_subnet = redis.CfnSubnetGroup(self,'subnet',
        #    cache_subnet_group_name="cache-private",
        #    #subnet_ids=
        #),ec2.Port.tcp()


        
        
        
            