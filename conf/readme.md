#Configuration HOWTO

Application configuration is done in a cascading fashion, with each of the values
defined in successive config files appending too (and possibly overwriting)
the total config context.

Definitions might be useful:

###ConfigContext
The overall config context. This is a single obecjt defined in global scope
which takes care of resolving what the configuration value should be. 

###All Configuration
*File: conf/all.py (required)*
Many configuration values are shared across all environments and scopes. The vast
majority of configuration should go here. 

###Environment Configuration
*File: depends on the environment variable ENV_NAME (required)*
Often times its useful to have configuration only for certain environments, or
possible overwrite some of the common stuff defined in all.py with config variables
pertinent to a given environment. These go here. 

###Local Configuration
*Files: local_pre.py, local.py (optional)*
Like environment configs, except they do not get checked into source control. This makes
them good for things like database passwords.

##Usage
To access configurations, do the following:

    import conf
    cfg = conf.get_context()
    
    if cfg.foo > 17: 
      print 'foorific!'

Note that for backwards compatibility, you can also conf.get('foo'), but that
format is depriciated and will not be supported in the future.

##Order/Precedence
The configration files are imported in the following order:

    local_pre
       |
       V
      all
       |
       V
    {env}.py
       |
       V
     local

Anything defined in a file that is imported afterwards is overwritten. Files defined in 
a previous step are accessed just like any other config variable.


