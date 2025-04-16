.DEFAULT_GOAL := help



# Variable check function (shell snippet)
check_vars = \
	if [ -z "$($(1))" ] || [ -z "$($(2))" ] || [ -z "$($(3))" ]; then \
		echo "❌ Missing required variables: $(1) and/or $(2) and/or $(3)"; \
		echo "👉 Showing help:"; \
		$(MAKE) help; \
		exit 1; \
	fi


timeSTAMP=$$(date "+%Y%m%d_%H%M")



# _ is a fake target used for fill redundant input requirement
_ = _


barevis: ## visual inspection of BareHexaboard. Used xml template data/template_BareHex_VisInspection.xml [inCSV=testsample_createXML_AssembledHexaBoard.csv]
	@$(call check_vars,inCSV,_,_)
	python3 createXML.py data/template_BareHex_VisInspection.xml $(inCSV) BareVis_$(timeSTAMP)
hexcreate: ## Create parts of AssembledHexaboard. Used xml template data/template_BareHex_VisInspection.xml [inCSV=testsample_createXML_AssembledHexaBoard.csv]
	@$(call check_vars,inCSV,_,_)
	python3 createXML.py data/template_BareHex_VisInspection.xml $(inCSV) NewHex_$(timeSTAMP)
hexvis: ## visual inspection of AssembledHexaboard. Used xml template data/template_BareHex_VisInspection.xml [inCSV=testsample_createXML_AssembledHexaBoard.csv]
	@$(call check_vars,inCSV,_,_)
	python3 createXML.py data/template_BareHex_VisInspection.xml $(inCSV) HexVis_$(timeSTAMP)
protomodulecreate: ## Create parts of proto module. Used xml template data/template_ProtoModule_CreatePart.xml  [inCSV=testsample_createXML_AssembledHexaBoard.csv]
	python3 createXML.py data/template_ProtoModule_CreatePart.xml $(inCSV) NewProtoModule_$(timeSTAMP)
simodulecreate: ## Create parts of silicon module. Used xml template data/template_SiModule_CreatePart.xml  [inCSV=testsample_createXML_AssembledHexaBoard.csv]
	python3 createXML.py data/template_SiModule_CreatePart.xml $(inCSV) NewProtoModule_$(timeSTAMP)


general: ## Create parts of AssembledHexaboard [inXML=data/template_AssembledHexaboard_CreatePart.xml] [inCSV=testsample_createXML_AssembledHexaBoard.csv] [oTAG=tag]
	@$(call check_vars,inXML,inCSV,oTAG)
	python3 createXML.py $(inXML) $(inCSV) $(oTAG)
check: ## check xml content [inXML=data/template_AssembledHexaboard_CreatePart.xml] [inCSV=testsample_createXML_AssembledHexaBoard.csv] [oTAG=tag]
	@$(call check_vars,inXML,inCSV,oTAG)
	python3 createXML.py $(inXML) $(inCSV) $(oTAG) 0


example: ## a example code to execute
	python3 createXML.py inputs/BareCreatePart_Nov26_2024_template.xml inputs/BareCreatePart_Nov26_2024.csv BareCreatePart_Nov26_2024 1




##@ Utility
IN_ARGS = [arg]
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
