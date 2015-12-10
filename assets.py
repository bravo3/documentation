from webassets.loaders import YAMLLoader

loader = YAMLLoader('source/_static/assets.yml')
env = loader.load_environment()

print "Building assets.."

js_assets = env['scripts'].urls()
css_assets = env['styles'].urls()

js_assets_rel = []
for asset in js_assets:
    print " - {}".format(asset)
    asset = '_static{}'.format(asset)
    js_assets_rel.append(asset)

css_assets_rel = []
for asset in css_assets:
    print " - {}".format(asset)
    asset = asset[1:]
    css_assets_rel.append(asset)

js = "{{% set script_files = ['{}'] %}}\n".format("', '".join(js_assets_rel))
css = "{{% set css_files = ['{}'] %}}\n".format("', '".join(css_assets_rel))

fp = open("source/_static/assets/assets.html", mode='w')
fp.writelines([js, css])
fp.close()

print "done"
