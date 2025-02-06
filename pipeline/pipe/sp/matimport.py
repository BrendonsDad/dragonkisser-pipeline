import substance_painter.resource as res
CONSTANT_FOR_SMART_MAT = [
	('rustMetal','G:/skyguard/prototypeAssets/02SmartMaterials/rustMetal.spsm', res.Usage.SMART_MATERIAL),
	("SG_AssortedMaterials","G:/skyguard/prototypeAssets/02SmartMaterials/SG_AssortedMaterials.spsm", res.Usage.SMART_MATERIAL),
	('SG_Brass','G:/skyguard/prototypeAssets/02SmartMaterials/SG_Brass.spsm', res.Usage.SMART_MATERIAL),
	('SG_Copper','G:/skyguard/prototypeAssets/02SmartMaterials/SG_Copper.spsm', res.Usage.SMART_MATERIAL),
	('SG_GradientMask','G:/skyguard/prototypeAssets/02SmartMaterials/SG_GradientMask.spsm', res.Usage.SMART_MATERIAL),
	('SG_Metal','G:/skyguard/prototypeAssets/02SmartMaterials/SG_Metal.spsm', res.Usage.SMART_MATERIAL),
	('SG_MetalBrushed','G:/skyguard/prototypeAssets/02SmartMaterials/SG_MetalBrushed.spsm', res.Usage.SMART_MATERIAL),
	('SG_MetalPainted','G:/skyguard/prototypeAssets/02SmartMaterials/SG_MetalPainted.spsm', res.Usage.SMART_MATERIAL),
	('SG_ShipOuterPaint','G:/skyguard/prototypeAssets/02SmartMaterials/SG_ShipOuterPaint.spsm', res.Usage.SMART_MATERIAL),
	('SM_WoodPlanks','G:/skyguard/prototypeAssets/02SmartMaterials/SM_WoodPlanks.spsm', res.Usage.SMART_MATERIAL), 
	('SG_Pipe','G:/skyguard/pipeline/gradientMasking/painter_old/SG_Pipe.spsm', res.Usage.SMART_MATERIAL), 
	('SG_GRM_Template', 'G:/skyguard/prototypeAssets/02SmartMaterials/SP_Export_Presets/SG_GRM_Template.spexp', res.Usage.EXPORT), 
	('SG_OcRMG_Template', 'G:/skyguard/prototypeAssets/02SmartMaterials/SP_Export_Presets/SG_OcRMG_Template.spexp', res.Usage.EXPORT), 
	('SG_OpRMG_Template', 'G:/skyguard/prototypeAssets/02SmartMaterials/SP_Export_Presets/SG_OpRMG_Template.spexp', res.Usage.EXPORT)
]
def isInstalled(material):
	pot = res.search(material[0])
	print(pot)
	if(len(pot)== 1):
		return True
	elif (len(pot) == 0):
		return False
	elif (len(pot) >1):
		print("Potential Error occured when installing:",material, "what the heck: More than one installed? Check naming conventions! These should be unique names!!!!!")
		return True

def install(installConst):
	
	# res.import_session_resource(installConst[1], installConst[2], installConst[0])
	res.import_project_resource(installConst[1], installConst[2], installConst[0])
	# res.Shelf.import_resource(installConst[1], res.Usage.SMART_MATERIAL, installConst[0])



def matImport():
	for mat in CONSTANT_FOR_SMART_MAT:
		print("".join(["Checking for ", mat[0], "..."]))
		if not isInstalled(mat):
			print("Installing...")
			install(mat)
			print("Installed!")
		else:
			print("Already Installed!")