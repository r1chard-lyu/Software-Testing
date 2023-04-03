
/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/Analysis/CallGraph.h"
#include "llvm/Transforms/Utils/Cloning.h"



using namespace llvm;
char LabPass::ID = 0;
bool LabPass::doInitialization(Module &M) {
    return true;
}

// printfPrototype form example 
static FunctionCallee printfPrototype(Module &M) { 
    LLVMContext &ctx = M.getContext();
    FunctionType *printfType = FunctionType::get(
      Type::getInt32Ty(ctx),          
      { Type::getInt8PtrTy(ctx) },    
      true);                          

    FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);
    return printfCallee;

}

// getI8StrVal form example 
static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();
  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}


// Creat Global Variable for save global variable
static GlobalVariable* createGlobalVariable(Module &M, StringRef name) {
  LLVMContext &ctx = M.getContext();  // Get the context of the module.

  // Create a constant integer value of 0.
  auto* nullConstant = Constant::getNullValue(IntegerType::getInt32Ty(ctx));

  // Create a new global variable with the null value and internal linkage.
  auto* nullGlobalVariable = new GlobalVariable(
      M, nullConstant->getType(), false, GlobalValue::InternalLinkage,
      nullConstant, name);

  return nullGlobalVariable;  // Return the created global variable.
}



bool LabPass::runOnModule(Module &M) {

  // Get a reference to the printf function prototype in the module.
  FunctionCallee printfCallee = printfPrototype(M);

  // Create a global variable to store the current depth of the call stack.
  GlobalVariable* depthGV = createGlobalVariable(M, "intDepth");

  // Iterate over each function in the module.
  for (auto &F : M){

    // Skip over any external function declarations.
    if(!F.isDeclaration()){

      // Print the name of the current function being processed.
      errs() << F.getName() << "\n";

      // Insert code at the beginning of the function to increment the call stack depth.
      IRBuilder<> BuilderEntry(&*F.getEntryBlock().getFirstInsertionPt());
      Value *ld = BuilderEntry.CreateLoad(BuilderEntry.getInt32Ty(), depthGV, depthGV->getName());
      Value *add = BuilderEntry.CreateAdd(ld, BuilderEntry.getInt32(1));
      BuilderEntry.CreateStore(add, depthGV);

      // Print the current call stack depth and function name.
      BuilderEntry.CreateCall( printfCallee, { getI8StrVal(M, "%*s", "strIndent"), ld, getI8StrVal(M, "", "strSpaces")} );
      BuilderEntry.CreateCall( printfCallee, { getI8StrVal(M, "%s: %p\n", "strAddr"), BuilderEntry.CreateGlobalStringPtr(F.getName()), &F });

      // Insert code at the end of the function to decrement the call stack depth.
      IRBuilder<> BuilderEnd(&*(--F.back().end()));
      Value *ld2 = BuilderEnd.CreateLoad(BuilderEnd.getInt32Ty(), depthGV, depthGV->getName());
      Value *sub = BuilderEnd.CreateSub(ld2, BuilderEnd.getInt32(1));
      BuilderEnd.CreateStore(sub, depthGV);

    }
  }
  return true;
}
static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);