CREATE TABLE ou_account(
    id INT NOT NULL   COMMENT '' ,
    usercode VARCHAR(32) NOT NULL   COMMENT '' ,
    username VARCHAR(32) NOT NULL   COMMENT '' ,
    passwd VARCHAR(32) NOT NULL   COMMENT '' ,
    email VARCHAR(32) NOT NULL   COMMENT '' ,
    userstatus VARCHAR(1) NOT NULL   COMMENT 'A/Active,I/Inavtive,F/Forbidden' ,
    deptcode VARCHAR(32) NOT NULL   COMMENT '' ,
    registeredtime VARCHAR(19) NOT NULL   COMMENT '' ,
    lastlogin VARCHAR(19)    DEFAULT  NULL COMMENT '' ,
    lastloginip VARCHAR(32)    DEFAULT  NULL COMMENT '' ,
    seqnum INT    DEFAULT  NULL COMMENT '' ,
    PRIMARY KEY (usercode)
)  COMMENT = '账号表';

CREATE TABLE ou_dept(
    id INT NOT NULL   COMMENT '' ,
    deptcode VARCHAR(32) NOT NULL   COMMENT '' ,
    pathcode VARCHAR(256) NOT NULL   COMMENT 'xxx/yyy/zzz' ,
    deptname VARCHAR(64) NOT NULL   COMMENT '' ,
    deptstatus VARCHAR(1) NOT NULL   COMMENT 'A/Active,I/Inactive' ,
    description VARCHAR(64)    DEFAULT  NULL COMMENT '' ,
    seqnum INT    DEFAULT  NULL COMMENT '' ,
    PRIMARY KEY (deptcode)
)  COMMENT = '部门表';

CREATE TABLE ou_resource(
    id INT NOT NULL   COMMENT '' ,
    resourcecode VARCHAR(128) NOT NULL   COMMENT '' ,
    resourcename VARCHAR(32) NOT NULL   COMMENT '' ,
    sysname VARCHAR(32) NOT NULL   COMMENT '' ,
    modelname VARCHAR(32) NOT NULL   COMMENT '' ,
    actionname VARCHAR(32) NOT NULL   COMMENT '' ,
    accesstype VARCHAR(1) NOT NULL   COMMENT 'L/login access,A/anonymous,R/role' ,
    PRIMARY KEY (resourcecode)
)  COMMENT = '资源表';

CREATE TABLE ou_role(
    id INT NOT NULL   COMMENT '' ,
    rolecode VARCHAR(32) NOT NULL   COMMENT '' ,
    rolename VARCHAR(32) NOT NULL   COMMENT '' ,
    description VARCHAR(64)    DEFAULT  NULL COMMENT '' ,
    seqnum INT    DEFAULT  NULL COMMENT '' ,
    PRIMARY KEY (rolecode)
)  COMMENT = '角色表';

CREATE TABLE ou_roleresource(
    id INT NOT NULL   COMMENT '' ,
    rolecode VARCHAR(32) NOT NULL   COMMENT '' ,
    resourcecode VARCHAR(128) NOT NULL   COMMENT '' ,
    rightflag VARCHAR(1) NOT NULL   COMMENT 'Y/Yes,N/No' ,
    PRIMARY KEY (rolecode,resourcecode,rightflag)
)  COMMENT = '角色资源表';

CREATE TABLE ou_userrole(
    id INT NOT NULL   COMMENT '' ,
    usercode VARCHAR(32) NOT NULL   COMMENT '' ,
    rolecode VARCHAR(32) NOT NULL   COMMENT '' ,
    PRIMARY KEY (usercode)
)  COMMENT = '用户角色表';

CREATE TABLE gl_dictionary(
    id INT NOT NULL   COMMENT '' ,
    typename VARCHAR(32) NOT NULL   COMMENT '' ,
    dickey VARCHAR(64) NOT NULL   COMMENT '' ,
    dicvalue VARCHAR(64) NOT NULL   COMMENT '' ,
    PRIMARY KEY (typename,dickey)
)  COMMENT = '系统字典表';

CREATE TABLE salaries_salary(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
    employeeid INT NOT NULL   COMMENT '' ,
    name VARCHAR(64) NOT NULL   COMMENT '' ,
    age INT NOT NULL   COMMENT '' ,
    department VARCHAR(64) NOT NULL   COMMENT '' ,
    hiredate VARCHAR(19) NOT NULL   COMMENT '' ,
    salary INT NOT NULL   COMMENT '' ,
    level INT NOT NULL   COMMENT '' ,
    subsidy Decimal(10)    DEFAULT  NULL COMMENT '' ,
    total Decimal(10)    DEFAULT  NULL COMMENT '' ,
    PRIMARY KEY (id)
)  COMMENT = '人员薪水表';

