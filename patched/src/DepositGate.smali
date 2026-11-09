.class public final Lcom/eip/netsniffer/DepositGate;
.super Ljava/lang/Object;
.source "DepositGate.kt"

# NOTE: stand-in for a class that was missing from the shipped dex files.
# Fail-open: nothing is locked and no redirect happens.

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/DepositGate;


# instance fields
.field private _ctx:Landroid/content/Context;

.field private final _needsRedirect:Landroidx/lifecycle/MutableLiveData;

.field private final _state:Landroidx/lifecycle/MutableLiveData;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/DepositGate;

    invoke-direct {v0}, Lcom/eip/netsniffer/DepositGate;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/DepositGate;->INSTANCE:Lcom/eip/netsniffer/DepositGate;

    return-void
.end method

.method private constructor <init>()V
    .locals 3

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    new-instance v0, Landroidx/lifecycle/MutableLiveData;

    new-instance v1, Lcom/eip/netsniffer/DepositGate$State;

    const/4 v2, 0x0

    invoke-direct {v1, v2}, Lcom/eip/netsniffer/DepositGate$State;-><init>(Ljava/lang/String;)V

    invoke-direct {v0, v1}, Landroidx/lifecycle/MutableLiveData;-><init>(Ljava/lang/Object;)V

    iput-object v0, p0, Lcom/eip/netsniffer/DepositGate;->_state:Landroidx/lifecycle/MutableLiveData;

    new-instance v0, Landroidx/lifecycle/MutableLiveData;

    const/4 v1, 0x0

    invoke-static {v1}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v1

    invoke-direct {v0, v1}, Landroidx/lifecycle/MutableLiveData;-><init>(Ljava/lang/Object;)V

    iput-object v0, p0, Lcom/eip/netsniffer/DepositGate;->_needsRedirect:Landroidx/lifecycle/MutableLiveData;

    return-void
.end method


# virtual methods
.method public final getNeedsRedirect()Landroidx/lifecycle/MutableLiveData;
    .locals 1

    iget-object v0, p0, Lcom/eip/netsniffer/DepositGate;->_needsRedirect:Landroidx/lifecycle/MutableLiveData;

    return-object v0
.end method

.method public final getState()Landroidx/lifecycle/MutableLiveData;
    .locals 1

    iget-object v0, p0, Lcom/eip/netsniffer/DepositGate;->_state:Landroidx/lifecycle/MutableLiveData;

    return-object v0
.end method

.method public final init(Landroid/content/Context;Ljava/lang/String;)V
    .locals 0

    iput-object p1, p0, Lcom/eip/netsniffer/DepositGate;->_ctx:Landroid/content/Context;

    return-void
.end method

.method public final isLocked(Ljava/lang/String;)Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final stateFor(Ljava/lang/String;)Landroidx/lifecycle/LiveData;
    .locals 1

    invoke-virtual {p0}, Lcom/eip/netsniffer/DepositGate;->getState()Landroidx/lifecycle/MutableLiveData;

    move-result-object v0

    return-object v0
.end method

.method public final tryExtract(Landroid/content/Context;Lcom/eip/netsniffer/NetEntry;)V
    .locals 0

    return-void
.end method
