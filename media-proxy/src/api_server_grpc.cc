/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Intel Corporation
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "api_server_grpc.h"

ConfigureServiceImpl::ConfigureServiceImpl(ProxyContext* ctx)
    : m_ctx(ctx)
{
}

Status ConfigureServiceImpl::TxStart(ServerContext* context, const TxControlRequest* request, ControlReply* reply)
{
    std::cout << "\nReceived command: TxStart." << std::endl;
    return Status::OK;
}

Status ConfigureServiceImpl::RxStart(ServerContext* context, const RxControlRequest* request, ControlReply* reply)
{
    std::cout << "\nReceived command: RxStart." << std::endl;
    return Status::OK;
}

Status ConfigureServiceImpl::TxStop(ServerContext* context, const StopControlRequest* request, ControlReply* reply)
{
    std::cout << "\nReceived command: Stop." << std::endl;
    return Status::OK;
}

Status ConfigureServiceImpl::RxStop(ServerContext* context, const StopControlRequest* request, ControlReply* reply)
{
    std::cout << "\nReceived command: Stop." << std::endl;
    return Status::OK;
}

Status ConfigureServiceImpl::Stop(ServerContext* context, const StopControlRequest* request, ControlReply* reply)
{
    std::cout << "\nReceived command: Stop." << std::endl;
    return Status::OK;
}

MsmDataPlaneServiceImpl::MsmDataPlaneServiceImpl(ProxyContext* ctx)
    : m_ctx(ctx)
{
}

Status MsmDataPlaneServiceImpl::stream_add_del(ServerContext* context, const StreamData* request, StreamResult* reply)
{
    return Status::OK;
}

HealthServiceImpl::HealthServiceImpl(ProxyContext* ctx)
    : m_ctx(ctx)
{
}

Status HealthServiceImpl::Check(ServerContext* context, const HealthCheckRequest* request, HealthCheckResponse* reply)
{
    reply->set_status(controller::HealthCheckResponse_ServingStatus_SERVING);

    return Status::OK;
}

Status HealthServiceImpl::Watch(ServerContext* context, const HealthCheckRequest* request, HealthCheckResponse* reply)
{
    return Status::OK;
}

void RunRPCServer(ProxyContext* ctx)
{
    ConfigureServiceImpl service(ctx);

    ServerBuilder builder;
    builder.AddListeningPort(ctx->getRPCListenAddress(), grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    INFO("gRPC Server listening on %s", ctx->getRPCListenAddress().c_str());

    server->Wait();
}
