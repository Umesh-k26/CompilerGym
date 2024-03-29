# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
if(NOT COMPILER_GYM_ENABLE_LLVM_ENV)
    return()
endif()

cg_add_all_subdirs()

cg_py_library(
  NAME
    llvm
  SRCS
    "__init__.py"
    "specs.py"
  DATA
    compiler_gym::envs::llvm::service::service
  DEPS
    ::benchmark_from_command_line
    ::compute_observation
    ::llvm_benchmark
    ::llvm_command_line
    ::llvm_env
    compiler_gym::util::util
  PUBLIC
)

cg_py_library(
  NAME benchmark_from_command_line
  SRCS benchmark_from_command_line.py
  DEPS
    compiler_gym::datasets::datasets
    compiler_gym::service::proto::proto
    compiler_gym::third_party::gccinvocation::gccinvocation
    compiler_gym::util::util
)

cg_py_library(
  NAME compute_observation
  SRCS compute_observation.py
  DATA compiler_gym::envs::llvm::service::compute_observation-files
  DEPS compiler_gym::util::util
)

cg_py_library(
  NAME
    lexed_ir
  SRCS
    "lexed_ir.py"
  PUBLIC
)

cg_py_library(
  NAME
    llvm_benchmark
  SRCS
    "llvm_benchmark.py"
  DEPS
    compiler_gym::datasets::datasets
    compiler_gym::errors::errors
    compiler_gym::service::proto::proto
    compiler_gym::third_party::llvm::llvm
    compiler_gym::util::util
  PUBLIC
)

cg_py_library(
  NAME
    llvm_command_line
  SRCS
    llvm_command_line.py
  DEPS
    compiler_gym::spaces::spaces
    compiler_gym::util::util
)

cg_py_library(
  NAME
    llvm_env
  SRCS
    "llvm_env.py"
  DEPS
    ::llvm_benchmark
    ::llvm_command_line
    ::llvm_rewards
    compiler_gym::datasets::datasets
    compiler_gym::errors::errors
    compiler_gym::service::client_service_compiler_env
    compiler_gym::envs::llvm::datasets::datasets
    compiler_gym::spaces::spaces
    compiler_gym::third_party::autophase::autophase
    compiler_gym::third_party::gccinvocation::gccinvocation
    compiler_gym::third_party::inst2vec::inst2vec
    compiler_gym::third_party::llvm::llvm
    compiler_gym::third_party::llvm::instcount
  PUBLIC
)

cg_py_library(
  NAME
    llvm_rewards
  SRCS
    "llvm_rewards.py"
  DEPS
    compiler_gym::service::service
    compiler_gym::spaces::spaces
    compiler_gym::util::util
    compiler_gym::views::views
  PUBLIC
)
