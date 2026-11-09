.class public final Lcom/eip/netsniffer/DepositLockOverlay;
.super Ljava/lang/Object;
.source "DepositLockOverlay.kt"

# NOTE: stand-in for a class that was missing from the shipped dex files.
# The original wrapped a fragment's root view in a "deposit required" overlay.
# Here the view is passed through untouched (fail-open).

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/DepositLockOverlay;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/DepositLockOverlay;

    invoke-direct {v0}, Lcom/eip/netsniffer/DepositLockOverlay;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/DepositLockOverlay;->INSTANCE:Lcom/eip/netsniffer/DepositLockOverlay;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final wrap(Landroidx/fragment/app/Fragment;Landroid/view/View;Ljava/lang/String;)Landroid/view/View;
    .locals 0

    return-object p2
.end method
