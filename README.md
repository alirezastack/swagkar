# Swagkar (Swagger Parser Utility)

Swagkar is a project aimed at importing a 3rd party Swagger file/url and getting information based on the OperationId and automatic handling of your requests without human intervention. All you need to know about your 3rd-part requests is just `operationId` and its required data payload.

### Installation Guide

Swagkar is an installable package. In order to install the package run the below command:

```bash
python3 setup.py install
```

By installing the package, few methods will be exposed to you. First method is called
`ok_swag_import` which is used to import your desired swagger YAML file.

Method usage is as follow:

```bash
ok_swag_import /path/to/your/api_spec.yml
```

The second method is called `ok_swag_call` which is used to call a remote API method.
In order to see its usage you can call the command with no parameter in terminal.

The overall usage is as follow:

```bash
ok_swag_call OperationId [param1=val1,...]
```

Sample call can be:

```bash
ok_swag_call CreateUser name=alireza&phone=09192654782
```

Before that you need to set an environment variable called `OK_SWAG_CONFIG` to your json configuration 
path like `/etc/ok_swag.json`:

```bash
export OK_SWAG_CONFIG=/etc/ok_swag.json
```

Please have a look at the configuration sample file called `config.sample.json` in order to know what is required configurations.