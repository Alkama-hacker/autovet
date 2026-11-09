.class public final Lcom/eip/netsniffer/TamperGuard;
.super Ljava/lang/Object;
.source "TamperGuard.kt"

# NOTE: stand-in for a class that was missing from the shipped dex files.
# Verification is a no-op here, so the app does not die on startup.

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/TamperGuard;


# instance fields
.field private _ctx:Landroid/content/Context;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/TamperGuard;

    invoke-direct {v0}, Lcom/eip/netsniffer/TamperGuard;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/TamperGuard;->INSTANCE:Lcom/eip/netsniffer/TamperGuard;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final init(Landroid/content/Context;)V
    .locals 0

    iput-object p1, p0, Lcom/eip/netsniffer/TamperGuard;->_ctx:Landroid/content/Context;

    return-void
.end method

.method public final isTampered()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final verify()Z
    .locals 1

    const/4 v0, 0x1

    return v0
.end method
