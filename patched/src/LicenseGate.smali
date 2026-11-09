.class public final Lcom/eip/netsniffer/LicenseGate;
.super Ljava/lang/Object;
.source "LicenseGate.kt"

# NOTE: this class was missing from the shipped dex files. This is a stand-in that
# keeps the original call-sites working. It never locks the UI (fail-open), so the app
# can start instead of crashing with NoClassDefFoundError.

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/LicenseGate;

.field private static final STATUS_LICENSED:Ljava/lang/String; = "LICENSED"


# instance fields
.field private _ctx:Landroid/content/Context;

.field private _state:Landroidx/lifecycle/MutableLiveData;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/LicenseGate;

    invoke-direct {v0}, Lcom/eip/netsniffer/LicenseGate;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/LicenseGate;->INSTANCE:Lcom/eip/netsniffer/LicenseGate;

    return-void
.end method

.method private constructor <init>()V
    .locals 3

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    new-instance v0, Landroidx/lifecycle/MutableLiveData;

    new-instance v1, Lcom/eip/netsniffer/LicenseGate$State;

    const-string v2, "LICENSED"

    invoke-direct {v1, v2, v2}, Lcom/eip/netsniffer/LicenseGate$State;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    invoke-direct {v0, v1}, Landroidx/lifecycle/MutableLiveData;-><init>(Ljava/lang/Object;)V

    iput-object v0, p0, Lcom/eip/netsniffer/LicenseGate;->_state:Landroidx/lifecycle/MutableLiveData;

    return-void
.end method


# virtual methods
.method public final getState()Landroidx/lifecycle/MutableLiveData;
    .locals 1

    iget-object v0, p0, Lcom/eip/netsniffer/LicenseGate;->_state:Landroidx/lifecycle/MutableLiveData;

    if-nez v0, :cond_0

    new-instance v0, Landroidx/lifecycle/MutableLiveData;

    invoke-direct {v0}, Landroidx/lifecycle/MutableLiveData;-><init>()V

    iput-object v0, p0, Lcom/eip/netsniffer/LicenseGate;->_state:Landroidx/lifecycle/MutableLiveData;

    :cond_0
    iget-object v0, p0, Lcom/eip/netsniffer/LicenseGate;->_state:Landroidx/lifecycle/MutableLiveData;

    return-object v0
.end method

.method public final init(Landroid/content/Context;Ljava/lang/String;)V
    .locals 0

    iput-object p1, p0, Lcom/eip/netsniffer/LicenseGate;->_ctx:Landroid/content/Context;

    return-void
.end method

.method public final isLocked()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final tryExtract(Landroid/content/Context;Lcom/eip/netsniffer/NetEntry;)V
    .locals 0

    return-void
.end method
