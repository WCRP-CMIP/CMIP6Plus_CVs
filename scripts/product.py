from __setup__ import * 

lddata = cmipld.sync(lddata)

name = 'product'

frame = {
        "@type": f"mip:core-descriptors",

        "@embed":"@always",
}



frame = cmipld.Frame(lddata,frame).clean(['rmld','untag'])

# data = cmipld.utils.sorted_dict(frame.key_value('name','description'))

data = frame.data
print(data)

# cmipld.utils.wjsn(finalise(data,name),base+f'/CMIP6Plus_{name}.json')