CXX = $(shell root-config --cxx)
LD = $(shell root-config --ld)

INC = $(shell pwd)
Repo = $(shell git rev-parse --show-toplevel)

CPPFLAGS := $(shell root-config --cflags) -I$(INC)/include 
LDFLAGS := $(shell root-config --glibs) $(STDLIBDIR) -lRooFit -lRooFitCore -L$(INC)/include 

CPPFLAGS += -g -std=c++11

TARGET1 = Fit2D 
TARGET2 = FitABCD

SRC1 = app/Fit2D.cc src/MakeFitMETTime.cc src/Aux.cc
SRC2 = app/FitABCD.cc src/MakeFitMETTime.cc src/Aux.cc

OBJ1 = $(SRC1:.cc=.o)
OBJ2 = $(SRC2:.cc=.o)

all : $(TARGET1) $(TARGET2)

$(TARGET1) : $(OBJ1)
	$(LD) $(CPPFLAGS) -o $(TARGET1) $(OBJ1) $(LDFLAGS)
	@echo $@
	@echo $<
	@echo $^

$(TARGET2) : $(OBJ2)
	$(LD) $(CPPFLAGS) -o $(TARGET2) $(OBJ2) $(LDFLAGS)
	@echo $@
	@echo $<
	@echo $^

%.o : %.cc
	$(CXX) $(CPPFLAGS) -o $@ -c $<
	@echo $@
	@echo $<

clean :
	rm -f *.o app/*.o src/*.o $(TARGET1) $(TARGET2) *~
