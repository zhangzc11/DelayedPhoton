CXX = $(shell root-config --cxx)
LD = $(shell root-config --ld)

INC = $(shell pwd)
Repo = $(shell git rev-parse --show-toplevel)

CPPFLAGS := $(shell root-config --cflags) -I$(INC)/include 
LDFLAGS := $(shell root-config --glibs) $(STDLIBDIR) -lRooFit -lRooFitCore -L$(INC)/include 

CPPFLAGS += -g -std=c++11

TARGET1 = Fit2D 

SRC1 = app/Fit2D.cc src/MakeFitMETTime.cc 

OBJ1 = $(SRC1:.cc=.o)

all : $(TARGET1)

$(TARGET1) : $(OBJ1)
	$(LD) $(CPPFLAGS) -o $(TARGET1) $(OBJ1) $(LDFLAGS)
	@echo $@
	@echo $<
	@echo $^

%.o : %.cc
	$(CXX) $(CPPFLAGS) -o $@ -c $<
	@echo $@
	@echo $<

clean :
	rm -f *.o app/*.o src/*.o $(TARGET1) *~
