interface
=========

Name your Interface what it is
------------------------------
If your interface is a Truck, call it Truck. Not ITruck because it isn’t an
ITruck it is a Truck. An Interface in Java is a Type. Then you have
implementations of DumpTruck, TransferTruck, WreckerTruck, CementTruck, etc.
When you are using the Interface Truck in place of a sub-class you just cast it
to Truck. As in List<Truck>. Putting I in front is just crappy Hungarian style
notation tautology that adds nothing but more stuff to type to your code.

All modern Java IDEs mark Interfaces and Implementations and what not without
this silly notation. Don’t call it TruckClass that is tautology just as bad as
the IInterface tautology.

The only real exception to this rule that I accept, and there are always
exceptions is AbstractTruck when the class is package local. Since only the
sub-classes will every see this and you should never cast to an Abstract class
it does add some information that the class is abstract and to how it should be
used. You could still come up with a better name than AbstractTruck and use
BaseTruck or DefaultTruck or some other more descriptive name instead. But
since Abstract classes should never be part of any public facing interface it
is an acceptable exception to the rule.

If it is an class it is an implementation
-----------------------------------------
And the Impl suffix is just more noise as well. More tautology. Anything that
isn’t an Interface is an Implementation, even Abstract classes which are just
partial implementations. Are you going to put that silly Impl suffix on every
name of every Class? It makes no more sense than suffixing every Class with
Class.

The Interface is a contract on what the public methods and properties have to
support, it is also Type information as well. Everything that implements Truck
is a Type of Truck.

Look to the Java standard library itself. Do you see IList, ArrayListImpl,
LinkedListImpl? No you see. List and ArrayList and LinkedList. Any of these
silly prefix/suffix naming conventions all violate the DRY principal as well.

Also if you find yourself adding DTO, JDO, BEAN or other silly repetitive
prefixes or suffixes to object names then they probably belong in a package
instead of all those suffixes. Properly packaged namespaces are self
documenting and reduce all the useless redundant information in these really
poorly conceived proprietary naming schemes that most places don’t even adhere
to in a consistent manner. If all you can come up with to make your Class name
unique is suffixing it with Impl, then you need to rethink having an Interface
at all. So when you have an situation where you have an Interface and a single
Implementation that is not uniquely specialized from the Interface you probably
don’t need the Interface.

If you can’t give unique descriptive names to your Interfaces and Classes, you
are doing it wrong.

Mocking the Mocking Argument
----------------------------
It has been argued that putting a Mock prefix or suffix on classes is a good
idiom to mark the classes as Mock implementations, why not call them MockImpl
if you are going to argue that?

Assuming that the real classes are in com.company.app.service. Mock
implementations should be in their own com.company.app.service.mock package,
ideally in a different directory structure with the Test classes, as in Maven,
which will allow them to have the same names as the non-Mock classes, and still
document that they are Mocks for testing only, and not pollute the name space
of the production code and make it easy to not-include that code in the
deployment.
