IPEFILELIST = $(shell find . -name "*.ipe")
PDFFILELIST = $(patsubst %.ipe,%.pdf,$(IPEFILELIST))
$(PDFFILELIST) : %.pdf : %.ipe
	iperender -pdf $< $@
.PHONY : ipetopdf
ipetopdf : $(PDFFILELIST)