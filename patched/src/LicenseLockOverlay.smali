.class public final Lcom/eip/netsniffer/LicenseLockOverlay;
.super Ljava/lang/Object;
.source "LicenseLockOverlay.kt"

# NOTE: stand-in for a class that was missing from the shipped dex files.
# The original wrapped a fragment's root view in a "license required" overlay.
# Here the view is passed through untouched (fail-open).

# static fields
.field public static final INSTANCE:Lcom/eip/netsniffer/LicenseLockOverlay;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/eip/netsniffer/LicenseLockOverlay;

    invoke-direct {v0}, Lcom/eip/netsniffer/LicenseLockOverlay;-><init>()V

    sput-object v0, Lcom/eip/netsniffer/LicenseLockOverlay;->INSTANCE:Lcom/eip/netsniffer/LicenseLockOverlay;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final wrap(Landroidx/fragment/app/Fragment;Landroid/view/View;)Landroid/view/View;
    .locals 0

    return-object p2
.end method
